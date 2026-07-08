"""
信息来源配置模块。

这里保存真实信息源配置。

fetch_sources.py 会从这些来源抓取 title、summary、url、source_name。
AI 生成简报时，只允许基于这些抓取结果总结，不允许自己编新闻。
"""


REQUIRED_FOLDERS = [
    "00_每日信息差简报",
    "01_AI新闻",
    "02_AI工具教程",
    "03_Codex使用技巧",
    "04_英文资料阅读",
    "05_德语学习",
    "06_电气自动化",
    "07_职业信息",
    "08_项目作品集",
    "09_模板",
    "99_归档",
]


SOURCE_CATEGORIES = ["AI新闻", "AI工具", "英文资料阅读"]


SOURCE_CONFIG = {
    "AI新闻": [
        {
            "type": "rss",
            "source_name": "Hugging Face Blog",
            "url": "https://huggingface.co/blog/feed.xml",
            "max_items": 3,
        },
        {
            "type": "rss",
            "source_name": "Google AI Blog",
            "url": "https://blog.google/technology/ai/rss/",
            "max_items": 3,
        },
        {
            "type": "rss",
            "source_name": "VentureBeat AI",
            "url": "https://venturebeat.com/category/ai/feed/",
            "max_items": 3,
        },
    ],
    "AI工具": [
        {
            "type": "web",
            "source_name": "DeepSeek API Docs",
            "url": "https://api-docs.deepseek.com/",
        },
        {
            "type": "web",
            "source_name": "OpenAI Platform Docs",
            "url": "https://platform.openai.com/docs/overview",
        },
        {
            "type": "web",
            "source_name": "GitHub Copilot Docs",
            "url": "https://docs.github.com/en/copilot",
        },
    ],
    "英文资料阅读": [
        {
            "type": "web",
            "source_name": "Python Documentation",
            "url": "https://docs.python.org/3/tutorial/introduction.html",
        },
        {
            "type": "web",
            "source_name": "MDN Web Docs",
            "url": "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/What_is_JavaScript",
        },
        {
            "type": "web",
            "source_name": "Siemens Industrial Automation",
            "url": "https://www.siemens.com/global/en/products/automation.html",
        },
    ],
}


def get_empty_source_data() -> dict:
    """返回空来源结构，用于抓取失败时生成来源不足版简报。"""
    return {
        "items": [],
        "by_category": {category: [] for category in SOURCE_CATEGORIES},
        "errors": [],
        "total_count": 0,
    }
