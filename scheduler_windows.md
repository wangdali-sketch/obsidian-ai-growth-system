# Windows 定时任务设置说明

这个文件教你把项目设置成每天自动运行。

推荐方式：让 Windows 任务计划程序运行 `run_daily.bat`，不要直接运行 `python main.py`。

这样做的好处是：

* 自动进入正确的项目目录。
* 自动激活虚拟环境，如果你以后创建了 `.venv` 或 `venv`。
* 自动创建 `logs` 文件夹。
* 每天把运行记录保存到 `logs\YYYY-MM-DD.log`。
* 不会打印 `.env` 文件内容。

## 1. 先手动测试 run_daily.bat

打开 PowerShell：

```powershell
cd C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system
.\run_daily.bat
```

运行后检查两个地方：

1. Obsidian 简报目录是否生成新文件：

```text
D:\obsidian-ai-growth-system\00_每日信息差简报
```

2. 项目日志目录是否生成当天日志：

```text
C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system\logs
```

日志文件名类似：

```text
2026-07-08.log
```

## 2. 打开任务计划程序

1. 按 `Win` 键。
2. 搜索 `任务计划程序`。
3. 打开它。

## 3. 创建基本任务

1. 点击右侧的 `创建基本任务`。
2. 名称填写：`Obsidian每日信息差简报`。
3. 描述填写：`每天自动抓取来源并生成 Obsidian 学习简报`。
4. 点击 `下一步`。

## 4. 设置触发时间

1. 选择 `每天`。
2. 设置运行时间，例如早上 `08:00`。
3. 点击 `下一步`。

## 5. 设置执行程序

选择 `启动程序`，然后填写：

程序或脚本：

```text
C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system\run_daily.bat
```

添加参数：

```text

```

起始于：

```text
C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system
```

注意：`起始于` 一定要填写代码项目文件夹路径，否则 Windows 可能找不到 `.env`、`main.py` 和日志目录。

## 6. 保存并测试

1. 点击 `完成`。
2. 在任务列表中找到 `Obsidian每日信息差简报`。
3. 右键点击它。
4. 选择 `运行`。
5. 等待 1-3 分钟。
6. 检查 `logs` 文件夹里的当天日志。
7. 检查 Obsidian 的 `00_每日信息差简报` 是否出现新简报。

## 7. 如何判断是否运行成功

打开当天日志，例如：

```text
C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system\logs\2026-07-08.log
```

看到类似内容，说明成功：

```text
运行成功，已生成每日简报：D:\obsidian-ai-growth-system\00_每日信息差简报\2026-07-08_每日信息差简报.md
退出代码：0
```

如果当天已经生成过，程序不会覆盖旧文件，而是生成：

```text
2026-07-08_每日信息差简报_v2.md
2026-07-08_每日信息差简报_v3.md
```

## 8. 常见问题

### 问题 1：任务运行了，但没有生成简报

先打开当天日志：

```text
C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system\logs
```

看里面有没有中文错误提示。

### 问题 2：日志里提示找不到 python

说明任务计划程序没有找到 Python。

解决方法：

1. 重新安装 Python，并勾选 `Add python.exe to PATH`。
2. 或者以后创建虚拟环境 `.venv`，让 `run_daily.bat` 自动激活虚拟环境。

### 问题 3：日志里显示抓取来源失败

可能是网络暂时不稳定，或者某个网站阻止抓取。

你可以单独运行：

```powershell
cd C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system
python fetch_sources.py
```

然后查看：

```text
C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system\debug_sources.md
```

### 问题 4：日志里显示 AI 生成失败

请检查 `.env`：

```text
C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system\.env
```

重点检查：

```text
LLM_PROVIDER
LLM_API_KEY
LLM_BASE_URL
LLM_MODEL
```

注意：不要把真实 API Key 发给别人，也不要把 `.env` 上传到 GitHub。

### 问题 5：会不会把 API Key 写进日志？

不会。`run_daily.bat` 不会打印 `.env` 文件内容。

如果 AI 调用报错，项目代码也会尽量清理错误信息，避免把 API Key 打印出来。
