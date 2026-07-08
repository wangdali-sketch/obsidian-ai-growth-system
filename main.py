"""
Obsidian 每日信息差简报生成器。

运行方式：
python main.py
"""

from datetime import datetime
from pathlib import Path
import sys

# 不生成 __pycache__ 缓存目录，避免新手误以为这是项目文件。
sys.dont_write_bytecode = True

from ai_client import generate_daily_report
from config import load_config
from fetch_sources import fetch_sources
from sources import REQUIRED_FOLDERS
from templates import render_insufficient_sources_report


DAILY_REPORT_FOLDER = "00_每日信息差简报"


def setup_console_output() -> None:
    """设置终端输出，避免 Windows 控制台遇到特殊字符时报编码错误。"""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")


def format_path_for_print(path: Path) -> str:
    """把路径转换成适合终端显示的文本。"""
    return str(path).replace("\u200b", "")


def check_vault_path(vault_path: Path) -> None:
    """检查 Obsidian 知识库路径是否存在。"""
    if not vault_path.exists():
        raise FileNotFoundError(f"Obsidian 知识库路径不存在：{format_path_for_print(vault_path)}")

    if not vault_path.is_dir():
        raise NotADirectoryError(f"Obsidian 知识库路径不是文件夹：{format_path_for_print(vault_path)}")


def create_required_folders(vault_path: Path) -> None:
    """创建项目需要的文件夹；已有文件夹不会被删除或覆盖。"""
    for folder_name in REQUIRED_FOLDERS:
        folder_path = vault_path / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)


def get_today_text() -> str:
    """返回今天日期，格式为 YYYY-MM-DD。"""
    return datetime.now().strftime("%Y-%m-%d")


def get_unique_report_path(vault_path: Path, today: str) -> Path:
    """生成不会覆盖已有文件的每日简报路径。"""
    report_folder = vault_path / DAILY_REPORT_FOLDER
    base_path = report_folder / f"{today}_每日信息差简报.md"

    if not base_path.exists():
        return base_path

    version = 2
    while True:
        version_path = report_folder / f"{today}_每日信息差简报_v{version}.md"
        if not version_path.exists():
            return version_path
        version += 1


def write_report(report_path: Path, content: str) -> None:
    """写入 Markdown 文件；如果文件已存在，就直接报错，避免误覆盖。"""
    if report_path.exists():
        raise FileExistsError(f"目标文件已存在，为避免覆盖已停止写入：{format_path_for_print(report_path)}")

    report_path.write_text(content, encoding="utf-8")


def main() -> int:
    """主程序入口。"""
    setup_console_output()

    try:
        config = load_config()
        vault_path = config.obsidian_vault_path

        check_vault_path(vault_path)
        create_required_folders(vault_path)

        today = get_today_text()
        print("开始抓取真实信息源...")
        source_data = fetch_sources(verbose=True)

        if source_data.get("total_count", 0) == 0:
            content = render_insufficient_sources_report(today, source_data)
            message = "本次抓取到 0 条真实信息源，未调用 AI。请检查 sources.py 或网络连接。"
        else:
            content, message = generate_daily_report(config, today, source_data)

        report_path = get_unique_report_path(vault_path, today)
        write_report(report_path, content)

        print(message)
        print(f"运行成功，已生成每日简报：{format_path_for_print(report_path)}")
        return 0

    except Exception as error:
        print(f"运行失败：{error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
