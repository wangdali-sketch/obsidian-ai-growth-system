"""
真实信息源抓取模块。

这个文件负责从 sources.py 配置的信息源里抓取真实内容。
抓取结果只保留四个核心字段：
title、summary、url、source_name。

运行方式：
python fetch_sources.py
"""

from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

from sources import SOURCE_CATEGORIES, SOURCE_CONFIG, get_empty_source_data


# 调试文件保存在代码项目目录，不放进 Obsidian 知识库。
PROJECT_DIR = Path(__file__).resolve().parent
DEBUG_FILE = PROJECT_DIR / "debug_sources.md"


def setup_console_output() -> None:
    """设置终端输出，避免 Windows 控制台中文显示报错。"""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")


def fetch_url(url: str, timeout: int = 20) -> str:
    """抓取网页文本；失败时把原因抛给上层处理。"""
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 obsidian-ai-growth-system source fetcher",
            "Accept": "text/html,application/rss+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )

    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw_data = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
        return raw_data.decode(charset, errors="replace")


def clean_text(text: str, max_length: int = 500) -> str:
    """清理 HTML 标签和多余空白。"""
    if not text:
        return ""

    text = unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) > max_length:
        return text[:max_length].rstrip() + "..."

    return text


def strip_xml_namespace(tag: str) -> str:
    """去掉 XML 命名空间，方便判断标签名。"""
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def child_text(element: ET.Element, child_name: str) -> str:
    """读取 RSS 或 Atom 子节点文本。"""
    for child in list(element):
        if strip_xml_namespace(child.tag) == child_name:
            return clean_text(child.text or "")
    return ""


def child_link(element: ET.Element) -> str:
    """读取 RSS 或 Atom 链接。"""
    for child in list(element):
        tag_name = strip_xml_namespace(child.tag)

        if tag_name == "link":
            href = child.attrib.get("href")
            if href:
                return href.strip()

            if child.text:
                return child.text.strip()

    return ""


def parse_feed(xml_text: str, category: str, source_name: str, max_items: int) -> list[dict]:
    """解析 RSS 或 Atom Feed。"""
    root = ET.fromstring(xml_text)
    root_name = strip_xml_namespace(root.tag)
    entries = []

    if root_name == "rss":
        channel = root.find("channel")
        if channel is not None:
            entries = channel.findall("item")
    elif root_name == "feed":
        entries = [item for item in list(root) if strip_xml_namespace(item.tag) == "entry"]

    results = []
    for entry in entries[:max_items]:
        title = child_text(entry, "title")
        url = child_link(entry)
        summary = child_text(entry, "description") or child_text(entry, "summary") or child_text(entry, "content")

        if not title or not url:
            continue

        results.append(
            {
                "category": category,
                "title": title,
                "summary": summary,
                "url": url,
                "source_name": source_name,
            }
        )

    return results


class MetaParser(HTMLParser):
    """从普通网页里读取 title 和 description。"""

    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.title_parts = []
        self.description = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """读取 title 和 meta description。"""
        attrs_dict = {key.lower(): value for key, value in attrs if value is not None}

        if tag.lower() == "title":
            self.in_title = True

        if tag.lower() == "meta":
            name = attrs_dict.get("name", "").lower()
            property_name = attrs_dict.get("property", "").lower()
            content = attrs_dict.get("content", "")

            if content and name == "description":
                self.description = content
            elif content and property_name == "og:description" and not self.description:
                self.description = content

    def handle_endtag(self, tag: str) -> None:
        """结束 title 读取。"""
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        """收集 title 文本。"""
        if self.in_title:
            self.title_parts.append(data)


def parse_web_page(html_text: str, category: str, source_name: str, url: str) -> list[dict]:
    """解析普通网页，提取标题和摘要。"""
    parser = MetaParser()
    parser.feed(html_text)

    title = clean_text(" ".join(parser.title_parts), max_length=160)
    summary = clean_text(parser.description, max_length=500)

    if not title:
        title = source_name

    return [
        {
            "category": category,
            "title": title,
            "summary": summary,
            "url": url,
            "source_name": source_name,
        }
    ]


def fetch_one_source(category: str, source: dict) -> tuple[list[dict], str | None]:
    """抓取单个来源，返回抓取结果和错误信息。"""
    source_type = source.get("type", "")
    source_name = source.get("source_name", "未知来源")
    url = source.get("url", "")

    if not url:
        return [], f"{source_name} 缺少 url 配置"

    try:
        text = fetch_url(url)

        if source_type == "rss":
            max_items = int(source.get("max_items", 3))
            return parse_feed(text, category, source_name, max_items), None

        if source_type == "web":
            return parse_web_page(text, category, source_name, url), None

        return [], f"{source_name} 使用了未知来源类型：{source_type}"

    except urllib.error.HTTPError as error:
        return [], f"{source_name} 抓取失败，HTTP 状态码：{error.code}，链接：{url}"
    except urllib.error.URLError as error:
        return [], f"{source_name} 抓取失败，网络错误：{error.reason}，链接：{url}"
    except Exception as error:
        return [], f"{source_name} 抓取失败：{error}，链接：{url}"


def build_source_data() -> dict:
    """抓取所有信息源，并整理成按分类分组的数据。"""
    source_data = get_empty_source_data()

    for category in SOURCE_CATEGORIES:
        for source in SOURCE_CONFIG.get(category, []):
            items, error = fetch_one_source(category, source)

            if error:
                source_data["errors"].append(error)

            for item in items:
                if item.get("title") and item.get("url") and item.get("source_name"):
                    source_data["items"].append(item)
                    source_data["by_category"][category].append(item)

    source_data["total_count"] = len(source_data["items"])
    return source_data


def write_debug_sources(source_data: dict) -> None:
    """把本次抓取结果写入 debug_sources.md。"""
    lines = ["# 本次抓取到的信息源", ""]

    for category in SOURCE_CATEGORIES:
        lines.append(f"## {category}")
        items = source_data["by_category"].get(category, [])

        if not items:
            lines.append("")
            lines.append("- 本分类本次未抓取到真实来源。")
            lines.append("")
            continue

        for item in items:
            lines.append(f"- 标题：{item['title']}")
            lines.append(f"  - 来源：{item['source_name']}")
            lines.append(f"  - 链接：{item['url']}")
            lines.append(f"  - 摘要：{item.get('summary') or '无摘要'}")
            lines.append("")

    if source_data["errors"]:
        lines.append("## 抓取失败记录")
        for error in source_data["errors"]:
            lines.append(f"- {error}")
        lines.append("")

    DEBUG_FILE.write_text("\n".join(lines), encoding="utf-8")


def print_fetch_summary(source_data: dict) -> None:
    """在终端打印抓取结果摘要。"""
    print(f"共抓取到 {source_data['total_count']} 条真实信息源。")

    for category in SOURCE_CATEGORIES:
        items = source_data["by_category"].get(category, [])
        print(f"{category}：{len(items)} 条")

        for item in items:
            print(f"- 标题：{item['title']}")
            print(f"  来源：{item['source_name']}")
            print(f"  链接：{item['url']}")

    if source_data["errors"]:
        print("抓取失败记录：")
        for error in source_data["errors"]:
            print(f"- {error}")

    print(f"调试文件已生成：{DEBUG_FILE}")


def fetch_sources(verbose: bool = True) -> dict:
    """抓取信息源、写调试文件，并按需打印摘要。"""
    source_data = build_source_data()
    write_debug_sources(source_data)

    if verbose:
        print_fetch_summary(source_data)

    return source_data


def main() -> int:
    """命令行入口：单独测试信息源抓取。"""
    setup_console_output()
    fetch_sources(verbose=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
