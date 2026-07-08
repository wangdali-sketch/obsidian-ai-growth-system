"""
AI 调用模块。

这里使用 OpenAI Python SDK，但不只支持 OpenAI 官方接口。
只要服务商提供 OpenAI 兼容 API，就可以通过 base_url 接入。

例如：
DeepSeek API、Xiaomi MiMo API。

没有 API Key 或调用失败时，自动返回模板版简报。
"""

import re

from templates import build_ai_prompt, render_template_report


def get_allowed_urls(source_data: dict) -> set[str]:
    """读取本次抓取到的真实来源链接。"""
    return {item["url"] for item in source_data.get("items", []) if item.get("url")}


def find_urls(markdown_text: str) -> set[str]:
    """从 Markdown 文本中找出 URL。"""
    urls = set()
    for match in re.findall(r"https?://[^\s)\]>\"]+", markdown_text):
        urls.add(match.rstrip(".,，。；;"))
    return urls


def validate_ai_output_sources(content: str, source_data: dict) -> tuple[bool, str]:
    """检查 AI 输出是否包含真实来源，且没有编造新链接。"""
    allowed_urls = get_allowed_urls(source_data)
    output_urls = find_urls(content)

    if not allowed_urls:
        return False, "本次没有可用真实来源链接。"

    if "**来源：**" not in content and "来源：" not in content:
        return False, "AI 输出缺少来源标记。"

    if not output_urls:
        return False, "AI 输出没有包含任何来源链接。"

    unknown_urls = output_urls - allowed_urls
    if unknown_urls:
        return False, f"AI 输出包含未抓取到的链接：{', '.join(sorted(unknown_urls))}"

    return True, "AI 输出来源检查通过。"


def sanitize_error_message(error: Exception, api_key: str) -> str:
    """清理错误信息，避免把 API Key 打印到终端。"""
    message = str(error)

    if api_key:
        message = message.replace(api_key, "***")

    return message


def generate_daily_report(config, today: str, source_data: dict) -> tuple[str, str]:
    """生成每日简报，并返回简报内容和运行提示。"""
    if not config.llm_api_key:
        content = render_template_report(today, source_data)
        return content, "未检测到 LLM_API_KEY，已生成模板版简报。"

    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=config.llm_api_key,
            base_url=config.llm_base_url,
        )
        prompt = build_ai_prompt(today, source_data)

        response = client.chat.completions.create(
            model=config.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": "你是适合大学生的 AI 学习教练，请用简体中文输出清晰、具体的 Markdown。",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        content = response.choices[0].message.content
        if not content:
            content = render_template_report(today, source_data)
            return content, "AI 返回内容为空，已改用模板版简报。"

        is_valid, validation_message = validate_ai_output_sources(content, source_data)
        if not is_valid:
            content = render_template_report(today, source_data)
            return content, f"{validation_message} 已改用来源版模板简报。"

        return (
            content.strip() + "\n",
            f"已通过 {config.llm_provider} 使用模型 {config.llm_model} 生成 AI 版简报。",
        )

    except Exception as error:
        content = render_template_report(today, source_data)
        safe_error = sanitize_error_message(error, config.llm_api_key)
        return content, f"AI 生成失败，已改用模板版简报。错误信息：{safe_error}"
