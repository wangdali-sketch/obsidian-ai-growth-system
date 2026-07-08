"""
Markdown 模板模块。

这里负责把资料拼成 Obsidian 可以直接打开的 Markdown 文本。
"""

import json


SOURCE_SHORTAGE_TEXT = "今日未抓取到足够真实来源，以下为学习建议，不代表新闻。"


def get_category_items(source_data: dict, category: str, limit: int | None = None) -> list[dict]:
    """按分类读取真实来源条目。"""
    items = source_data.get("by_category", {}).get(category, [])

    if limit is None:
        return items

    return items[:limit]


def format_source_link(item: dict) -> str:
    """生成 Markdown 来源链接。"""
    return f"**来源：** [{item['source_name']}]({item['url']})"


def render_template_report(today: str, source_data: dict) -> str:
    """生成不依赖 API Key 的来源版每日简报。"""
    if source_data.get("total_count", 0) == 0:
        return render_insufficient_sources_report(today, source_data)

    news_blocks = []
    news_items = get_category_items(source_data, "AI新闻", limit=3)
    for index, item in enumerate(news_items, start=1):
        news_blocks.append(
            f"""### {index}. {item["title"]}

* 标题：{item["title"]}
* 简短说明：{item["summary"]}
* 为什么值得关注：这是一条来自真实来源的信息，可以作为今天了解 AI 行业动态的入口。
* 对普通大学生有什么启发：先读标题和摘要，再打开来源链接核对原文，不要只看二手总结。
* {format_source_link(item)}"""
        )

    if not news_blocks:
        news_text = SOURCE_SHORTAGE_TEXT
    else:
        news_text = "\n\n".join(news_blocks)

    tool_items = get_category_items(source_data, "AI工具", limit=1)
    if tool_items:
        tool = tool_items[0]
        tool_text = f"""* 工具名称：{tool["title"]}
* 它能做什么：请先打开来源链接查看官方说明，再结合自己的学习任务判断用途。
* 我这个中德电气自动化学生可以怎么用：可以把它当作学习 AI 工具、API 文档阅读和自动化项目扩展的材料。
* 今天可以尝试的一个小操作：打开来源链接，记录 3 个你看懂的功能点和 1 个没看懂的问题。
* {format_source_link(tool)}"""
    else:
        tool_text = f"{SOURCE_SHORTAGE_TEXT}\n\n* 来源不足：本次没有抓取到 AI 工具类真实来源。"

    english_items = get_category_items(source_data, "英文资料阅读", limit=1)
    if english_items:
        english = english_items[0]
        english_text = f"""* 英文原句或英文短段落：{english["summary"] or english["title"]}
* 中文解释：这段内容来自真实英文资料，建议先理解标题，再打开原文阅读上下文。
* 关键词：请从原文里挑出 3-5 个技术词汇，例如 API、automation、model、tool、documentation。
* 我应该怎么读懂它：先读标题，再读摘要，最后打开来源链接看原文第一段。
* {format_source_link(english)}"""
    else:
        english_text = f"{SOURCE_SHORTAGE_TEXT}\n\n* 来源不足：本次没有抓取到英文资料阅读类真实来源。"

    return f"""# {today} 每日信息差简报

> 说明：这是一篇来源版简报。所有新闻、工具和英文阅读内容都必须来自本次抓取到的真实来源。

## 1. 今天值得关注的 AI 新闻

{news_text}

## 2. 今天推荐学习的 AI 工具

{tool_text}

## 3. 今天的 Codex 使用技巧

* 技巧名称：先让 Codex 看来源，再让它总结
* 使用场景：当你想让 AI 写新闻简报、资料摘要或学习卡片时。
* 示例提示词：请只基于我提供的标题、摘要、链接和来源名称总结，不要编造来源中没有的信息。
* 注意事项：没有来源链接的内容只能当学习建议，不能当新闻。

## 4. 今天的英文资料阅读

{english_text}

## 5. 这对我有什么用

今天的信息和你最直接的关系是：你不只是看 AI 总结，而是在练习“先看来源，再做判断”。

它对你学习 AI、Codex、英语和职业规划的帮助：

* 学 AI：用真实来源建立判断力，减少被假新闻带偏。
* 学 Codex：练习让 AI 基于材料总结，而不是让 AI 自由发挥。
* 学英语：从真实英文网页里积累技术词汇。
* 做职业规划：以后面试时可以展示你如何搭建“可追溯来源”的知识库系统。

值得保存进知识库的内容：

* 带来源链接的 AI 新闻
* 官方工具文档链接
* 英文技术资料阅读记录

## 6. 今天可以做的一个小任务

用 15-30 分钟完成这个任务：

1. 打开今天生成的这篇简报。
2. 随机点开 1 个来源链接。
3. 检查简报内容是否真的来自这个来源。
4. 在 Obsidian 里写一句：这个来源对我有什么用。

## 7. 值得保存进知识库的内容

* [[AI新闻_带来源阅读]]
* [[AI工具_官方文档阅读]]
* [[Codex技巧_只基于来源总结]]
* [[英文资料阅读_真实来源精读]]

## 8. 明天继续关注什么

* 继续检查每条 AI 新闻是否有真实来源链接。
* 优先阅读官方文档和一手资料。
* 把一个真实来源整理成单独知识卡片。
"""


def render_insufficient_sources_report(today: str, source_data: dict) -> str:
    """生成来源不足版简报，不把学习建议伪装成新闻。"""
    errors = source_data.get("errors", [])
    if errors:
        error_text = "\n".join(f"* {error}" for error in errors)
    else:
        error_text = "* 本次没有记录到具体错误，可能是来源配置为空或网络不可用。"

    return f"""# {today} 每日信息差简报

> {SOURCE_SHORTAGE_TEXT}

## 1. 今天值得关注的 AI 新闻

来源不足：本次没有抓取到可验证的 AI 新闻来源，所以这里不生成新闻。

## 2. 今天推荐学习的 AI 工具

来源不足：本次没有抓取到可验证的 AI 工具来源，所以这里不推荐具体工具新闻。

## 3. 今天的 Codex 使用技巧

* 技巧名称：先验证来源，再生成内容
* 使用场景：让 Codex 写新闻、日报、行业简报时。
* 示例提示词：请只基于我提供的真实链接总结。如果没有链接，请明确写来源不足。
* 注意事项：没有来源链接的内容不能当新闻看。

## 4. 今天的英文资料阅读

来源不足：本次没有抓取到可验证的英文资料来源，所以这里不生成英文原文摘录。

## 5. 这对我有什么用

这次最重要的收获是：知识库不是内容越多越好，而是内容要能追溯来源。

如果没有来源链接，就只能把它当成学习建议，不能当成真实新闻或行业事实。

## 6. 今天可以做的一个小任务

用 15-30 分钟完成这个任务：

1. 打开代码项目里的 `sources.py`。
2. 检查里面的信息源链接是否能在浏览器打开。
3. 单独运行 `python fetch_sources.py`。
4. 打开 `debug_sources.md` 查看抓取结果。

## 7. 值得保存进知识库的内容

* [[信息源验证_为什么要看来源链接]]
* [[Codex技巧_没有来源就不要写新闻]]

## 8. 明天继续关注什么

* 检查 `sources.py` 里的 RSS 或网页来源是否稳定。
* 优先添加官方博客、官方文档和可信技术媒体。
* 继续完善来源验证流程。

## 抓取失败记录

{error_text}
"""


def build_ai_prompt(today: str, source_data: dict) -> str:
    """生成发给 AI 的提示词。"""
    allowed_sources = []
    for item in source_data.get("items", []):
        allowed_sources.append(
            {
                "category": item.get("category", ""),
                "title": item.get("title", ""),
                "summary": item.get("summary", ""),
                "url": item.get("url", ""),
                "source_name": item.get("source_name", ""),
            }
        )

    allowed_sources_text = json.dumps(allowed_sources, ensure_ascii=False, indent=2)

    return f"""请为一名“中德电气自动化技术专业大学生”生成一篇 Obsidian Markdown 每日信息差简报。

日期：{today}

学生背景：
普通大学生，正在学习 AI、Codex、德语、英语资料阅读和电气自动化，希望抹平 AI 与职业信息差，并长期形成个人知识库和面试作品集。

最重要的来源规则：
1. 你只能使用下面“允许使用的真实信息源”里的 title、summary、url、source_name、category。
2. 不允许编造来源中没有的新闻。
3. 不允许编造链接。
4. 不允许编造产品发布、公司计划、融资、模型能力或发布日期。
5. 每条 AI 新闻、AI 工具、英文资料阅读内容都必须包含这一行：**来源：** [来源名称](链接)
6. 如果某个分类来源不足，就写“来源不足”，不要硬编。
7. 如果来源中没有的信息，不要写成事实。

允许使用的真实信息源：
{allowed_sources_text}

请严格使用以下 Markdown 结构，不要添加额外一级标题：

# {today} 每日信息差简报

## 1. 今天值得关注的 AI 新闻
从 category 为“AI新闻”的来源中总结最多 3 条。每条包括：标题、简短说明、为什么值得关注、对普通大学生有什么启发、**来源：** [来源名称](链接)。
如果没有足够来源，必须写：来源不足。

## 2. 今天推荐学习的 AI 工具
从 category 为“AI工具”的来源中介绍 1 个 AI 工具或 AI 软件功能。包括：工具名称、它能做什么、我这个中德电气自动化学生可以怎么用、今天可以尝试的一个小操作、**来源：** [来源名称](链接)。
如果没有来源，必须写：来源不足。

## 3. 今天的 Codex 使用技巧
给 1 个技巧。包括：技巧名称、使用场景、示例提示词、注意事项。

## 4. 今天的英文资料阅读
从 category 为“英文资料阅读”的来源中提供 1 段适合阅读的英文 AI 或技术资料摘要。包括：英文原句或英文短段落、中文解释、关键词、我应该怎么读懂它、**来源：** [来源名称](链接)。
如果没有来源，必须写：来源不足。

## 5. 这对我有什么用
用非常接地气的方式解释今天的信息和学生有什么关系，以及对 AI、Codex、英语、职业规划有什么帮助。

## 6. 今天可以做的一个小任务
给一个 15-30 分钟能完成的小任务，简单、具体、可执行。

## 7. 值得保存进知识库的内容
列出知识卡片标题，使用 Obsidian 双链格式。

## 8. 明天继续关注什么
最多 3 条。

要求：
1. 全文使用简体中文。
2. 语言适合编程初学者，不要写得太抽象。
3. 内容要和 AI、Codex、英语阅读、电气自动化、职业发展有关。
4. 输出必须是纯 Markdown，不要包裹代码块。
5. 所有 Markdown 链接必须来自“允许使用的真实信息源”里的 url，不能新增其他链接。
"""
