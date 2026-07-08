# obsidian-ai-growth-system

这是一个适合“中德电气自动化技术专业大学生”的 Obsidian 个人信息差知识库自动化项目。

它会用 Python 每天生成一篇 Markdown 格式的“每日信息差简报”，帮助你长期积累 AI、Codex、英语资料阅读、电气自动化和职业信息。

项目使用 OpenAI 兼容 API 格式，不只支持 OpenAI 官方接口，也可以接入 DeepSeek API、Xiaomi MiMo API 等服务。

代码项目和 Obsidian 知识库是分开的：

* 代码项目目录：`C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system`
* Obsidian 知识库目录：`D:\obsidian-ai-growth-system`

## 适合谁用

这个项目适合：

* 正在学习 AI 和 Codex 的大学生
* 想提高英文技术资料阅读能力的学生
* 电气自动化、自动化、机电、电气类专业学生
* 想把个人知识库做成面试作品集的人
* Python 基础还不强，但想做一个真实自动化项目的人

## 项目文件结构

```text
代码项目文件夹
├─ .github
│  └─ workflows
│     └─ daily-brief.yml
├─ main.py
├─ config.py
├─ templates.py
├─ sources.py
├─ fetch_sources.py
├─ ai_client.py
├─ run_daily.bat
├─ requirements.txt
├─ .env.example
├─ debug_sources.md
├─ logs
└─ scheduler_windows.md
```

## 每个代码文件是做什么的

* `main.py`：主程序，运行后生成当天的每日信息差简报。
* `config.py`：读取 Obsidian 路径、模型服务商、API Key、接口地址和模型名称。
* `templates.py`：保存 Markdown 模板和 AI 提示词模板。
* `sources.py`：保存 Obsidian 文件夹列表和真实信息源配置。
* `fetch_sources.py`：抓取真实来源，生成 `debug_sources.md`，并在终端打印抓取摘要。
* `ai_client.py`：封装 OpenAI 兼容 API 调用逻辑。没有 API Key 时自动返回模板版简报。
* `run_daily.bat`：Windows 一键运行脚本，适合手动双击或任务计划程序每天自动执行。
* `.github/workflows/daily-brief.yml`：GitHub Actions 云端自动运行配置。
* `logs`：保存每天运行日志，例如 `logs\2026-07-08.log`。

## 安装依赖

先打开 PowerShell，进入代码项目文件夹：

```powershell
cd C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system
```

安装依赖：

```powershell
pip install -r requirements.txt
```

如果你暂时没有 API Key，也可以先直接运行 `python main.py`。模板版简报不依赖真实 AI API。

## 配置 .env

复制 `.env.example`，新建一个 `.env` 文件。

`.env` 用来保存你的本地配置，尤其是 API Key。

注意：

* API Key 只能写在 `.env` 里，不要写进 Python 代码。
* 不要把真实 `.env` 发给别人。
* 不要把真实 `.env` 上传到 GitHub。
* 项目已经用 `.gitignore` 忽略 `.env`，只保留 `.env.example` 作为示例。

## DeepSeek API 配置示例

把 `.env` 改成类似这样：

```text
OBSIDIAN_VAULT_PATH=D:\obsidian-ai-growth-system

LLM_PROVIDER=deepseek
LLM_API_KEY=你的DEEPSEEK_API_KEY
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-v4-flash
```

说明：

* `OBSIDIAN_VAULT_PATH`：你的 Obsidian 知识库路径。
* `LLM_PROVIDER`：模型服务商名称，方便终端提示你当前用的是谁。
* `LLM_API_KEY`：你的 API Key。没有可以先留空。
* `LLM_BASE_URL`：OpenAI 兼容 API 地址。
* `LLM_MODEL`：模型名称。

## Xiaomi MiMo API 配置示例

把 `.env` 改成类似这样：

```text
OBSIDIAN_VAULT_PATH=D:\obsidian-ai-growth-system

LLM_PROVIDER=mimo
LLM_API_KEY=你的MIMO_API_KEY
LLM_BASE_URL=https://api.xiaomimimo.com/v1
LLM_MODEL=mimo-v2.5-pro
```

说明：

* `LLM_PROVIDER=mimo`：表示你当前使用 Xiaomi MiMo。
* `LLM_BASE_URL`：填写 MiMo 的 OpenAI 兼容接口地址。
* `LLM_MODEL`：填写 MiMo 支持的模型名称。

如果服务商以后调整了接口地址或模型名，只需要改 `.env`，不用改代码。

## 如何运行

在 PowerShell 中运行：

```powershell
cd C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system
python main.py
```

程序运行顺序是：

1. 先运行真实信息源抓取。
2. 在终端打印抓取到多少条来源。
3. 把抓取结果写入 `debug_sources.md`。
4. 再调用 AI 生成每日简报。
5. 如果抓取到 0 条真实来源，就不调用 AI，直接生成“来源不足版简报”。

运行成功后，终端会显示生成的文件路径，例如：

```text
运行成功，已生成每日简报：D:\obsidian-ai-growth-system\00_每日信息差简报\2026-07-08_每日信息差简报.md
```

如果 API 调用成功，终端会看到类似：

```text
已通过 deepseek 使用模型 deepseek-v4-flash 生成 AI 版简报。
```

如果 API Key 没填，或者 API 调用失败，程序不会崩溃，会自动生成模板版简报。

## 如何手动运行 run_daily.bat

推荐日常使用这个方式：

```powershell
cd C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system
.\run_daily.bat
```

`run_daily.bat` 会自动做这些事：

* 进入代码项目目录。
* 如果发现 `.venv` 或 `venv`，自动激活虚拟环境。
* 如果没有 `logs` 文件夹，自动创建。
* 运行 `python main.py`。
* 把运行日志写入当天日志文件。

日志文件位置：

```text
C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system\logs\YYYY-MM-DD.log
```

例如：

```text
C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system\logs\2026-07-08.log
```

注意：`run_daily.bat` 不会打印 `.env` 文件内容，所以不会主动把 API Key 写进日志。

## 如何单独测试信息源抓取

如果你只想测试信息源，不想生成每日简报，可以运行：

```powershell
cd C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system
python fetch_sources.py
```

终端会显示：

* 共抓取多少条
* 每个分类多少条
* 每条的标题
* 来源名称
* 来源链接
* 抓取失败原因

## 如何查看 debug_sources.md

每次运行 `fetch_sources.py` 或 `main.py` 后，都会更新这个文件：

```text
C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system\debug_sources.md
```

你可以用记事本或 VS Code 打开它。

它里面会列出本次抓取到的真实信息源，例如：

```text
标题：
来源：
链接：
摘要：
```

如果某个来源抓取失败，也会记录失败原因。

## 如何判断简报是否基于真实来源

打开 Obsidian 里的每日简报，重点检查三处：

* `今天值得关注的 AI 新闻`
* `今天推荐学习的 AI 工具`
* `今天的英文资料阅读`

每条内容都应该能看到这种格式：

```markdown
**来源：** [来源名称](链接)
```

如果某条内容没有来源链接，就不要把它当新闻看。

## 为什么没有来源链接的内容不能当新闻看

AI 可能会把常识、推测和真实新闻混在一起写。

所以这个项目现在强制要求：

* 没有真实链接，不写成新闻。
* 链接必须来自 `fetch_sources.py` 抓到的结果。
* AI 不能自己编来源。
* 如果来源不足，简报会明确写“来源不足”。

这样做的目的不是让内容看起来更多，而是让你的知识库更可信。

## 如何查看生成结果

打开 Obsidian，然后进入：

```text
00_每日信息差简报
```

你会看到类似这样的文件：

```text
2026-07-08_每日信息差简报.md
```

如果当天已经运行过，再次运行不会覆盖旧文件，而是生成：

```text
2026-07-08_每日信息差简报_v2.md
```

## 如何设置 Windows 定时任务

详细步骤请看：

```text
scheduler_windows.md
```

最关键的三个设置是：

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

设置完成后，在任务计划程序里右键这个任务，选择 `运行`。

运行后检查：

1. `logs` 文件夹里是否出现当天日志。
2. 日志里是否出现 `运行成功，已生成每日简报`。
3. Obsidian 的 `00_每日信息差简报` 是否出现新文件。

## 如果没生成简报怎么排查

先看当天日志：

```text
C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system\logs
```

常见情况：

* 日志提示找不到 `python`：说明 Python 没进 PATH，需要重新安装 Python，或创建虚拟环境。
* 日志提示 Obsidian 路径不存在：检查 `.env` 里的 `OBSIDIAN_VAULT_PATH`。
* 日志提示抓取来源失败：运行 `python fetch_sources.py`，然后查看 `debug_sources.md`。
* 日志提示 AI 生成失败：检查 `.env` 里的 `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`。
* 日志显示来源不足：说明当天没有抓到可用真实来源，不要把学习建议当新闻。

## 常见问题

### 1. 没有 API Key 能不能用？

可以。程序会生成模板版每日简报，适合先测试流程。

### 2. 会不会覆盖我已有的 Obsidian 文件？

不会。程序只会创建需要的文件夹和新的每日简报文件。当天文件已存在时，会自动加版本号。

### 3. 提示 Obsidian 路径不存在怎么办？

检查 `.env` 里的 `OBSIDIAN_VAULT_PATH` 是否写对。

Windows 路径示例：

```text
D:\obsidian-ai-growth-system
```

### 4. 我以后怎么扩展这个项目？

你可以从简单功能开始：

* 在 `sources.py` 里加入你常看的 AI 网站、RSS 或官方文档。
* 在 `templates.py` 里调整每日简报结构。
* 在 `09_模板` 文件夹里保存自己的学习模板。
* 把生成的好内容整理成单独知识卡片。

## 建议的学习方法

每天不要只看简报，建议做一个小动作：

1. 选一条 AI 新闻，写一句自己的理解。
2. 选一个英文句子，整理 3 个关键词。
3. 选一个 Codex 技巧，真的用一次。
4. 把有价值的内容保存成 Obsidian 双链知识卡片。

这样坚持一段时间后，这个知识库就不只是笔记，而是你的学习记录和面试作品集。

## GitHub Actions 云端自动运行

这个功能解决的问题是：就算你的 Windows 电脑关机，GitHub 也可以每天在云端运行一次 `python main.py`，生成新的每日信息差简报 Markdown，并提交回 GitHub 仓库。

本地运行和云端运行的区别：

* 本地运行：读取 `.env` 里的 `OBSIDIAN_VAULT_PATH`，写入你的本地 Obsidian 知识库。
* 云端运行：检测到 `GITHUB_ACTIONS=true` 后，不使用本地绝对路径，直接写入当前 GitHub 仓库里的 `00_每日信息差简报/`。

### 1. 为什么电脑关机也能运行

GitHub Actions 运行在 GitHub 的服务器上，不依赖你的电脑。

只要代码已经上传到 GitHub，GitHub 到时间就会自动启动一台临时云端机器，执行 workflow 里的步骤。

当前配置是每天北京时间 08:00 运行一次。GitHub cron 使用 UTC 时间，所以 workflow 里写的是：

```yaml
schedule:
  - cron: "0 0 * * *"
```

### 2. 如何把项目上传到 GitHub

如果这是第一次上传，先在 GitHub 网站新建一个空仓库，然后在本地项目目录运行：

```powershell
cd C:\Users\tgf\Documents\Codex\obsidian-ai-growth-system
git init
git add .
git commit -m "init obsidian ai growth system"
git branch -M main
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```

注意：

* 不要提交 `.env`。
* `.gitignore` 已经包含 `.env`、`__pycache__/`、`logs/`。
* 如果 Git 提示 `.env` 被加入暂存区，先运行 `git restore --staged .env`，再重新提交。

### 3. 如何配置 GitHub Secrets

打开你的 GitHub 仓库页面，按这个路径进入：

```text
Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

需要添加 4 个 Secrets：

```text
LLM_PROVIDER
LLM_API_KEY
LLM_BASE_URL
LLM_MODEL
```

DeepSeek 示例：

```text
LLM_PROVIDER=deepseek
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-v4-flash
```

MiMo 示例：

```text
LLM_PROVIDER=mimo
LLM_BASE_URL=https://api.xiaomimimo.com/v1
LLM_MODEL=mimo-v2.5-pro
```

`LLM_API_KEY` 填你自己的真实 API Key。不要把真实 API Key 写进 README，也不要提交到 GitHub。

### 4. 如何手动运行 Actions 测试

上传代码并配置 Secrets 后，可以先手动测试一次：

1. 打开 GitHub 仓库页面。
2. 点击 `Actions`。
3. 点击左侧 `每日信息差简报`。
4. 点击右侧 `Run workflow`。
5. 选择 `main` 分支。
6. 再点击绿色的 `Run workflow`。

手动运行会真的生成一篇 Markdown。如果当天已经有文件，程序会自动生成 `_v2`、`_v3` 这样的版本号，不会覆盖旧文件。

### 5. 如何查看运行日志

查看日志步骤：

1. 打开 GitHub 仓库页面。
2. 点击 `Actions`。
3. 点击某一次运行记录。
4. 点击任务 `生成并提交每日信息差简报`。
5. 展开失败或成功的步骤查看输出。

常看的步骤：

* `安装依赖`：检查 `requirements.txt` 是否能正常安装。
* `运行每日简报脚本`：检查信息源抓取、AI 调用、Markdown 生成是否成功。
* `提交新生成的 Markdown 简报`：检查是否成功 commit 和 push。

### 6. 如何确认简报已经生成

运行成功后，在 GitHub 仓库里检查：

```text
00_每日信息差简报/
```

你应该能看到类似这样的文件：

```text
2026-07-08_每日信息差简报.md
2026-07-08_每日信息差简报_v2.md
```

如果 Actions 日志显示“没有新的 Markdown 简报需要提交”，说明本次没有检测到新增文件。正常情况下，`main.py` 每次都会按日期和版本号生成一个新文件。

### 7. 如何让 Obsidian 同步 GitHub 仓库里的新笔记

简单做法有两种：

第一种：把 GitHub 仓库克隆到本地，然后用 Obsidian 打开这个仓库文件夹。

```powershell
git clone https://github.com/你的用户名/你的仓库名.git D:\obsidian-ai-growth-system
```

以后每天打开电脑后，在这个文件夹里运行：

```powershell
git pull
```

第二种：继续使用你现在的 Obsidian 知识库，把 GitHub 仓库也放在同一个知识库目录里，或者使用 Obsidian Git 插件自动 pull。

新手建议先用第一种，因为路径最清楚，也最容易排查。

### 8. 常见问题排查

问题：Actions 提示没有权限 push。

处理：检查 workflow 里是否有：

```yaml
permissions:
  contents: write
```

问题：Actions 运行成功，但没有看到 AI 版内容。

处理：检查 GitHub Secrets 里有没有 `LLM_API_KEY`，名字必须完全一致。没有 API Key 时，程序会生成模板版简报，不会崩溃。

问题：Actions 生成的是来源不足版简报。

处理：说明云端这次没有抓到可用信息源。打开运行日志，看 `运行每日简报脚本` 里的抓取失败记录，再检查 `sources.py` 里的链接是否可访问。

问题：本地能写 Obsidian，云端写不到本地 Obsidian。

处理：这是正常的。GitHub 云端不能访问你电脑里的 `D:\obsidian-ai-growth-system`。云端只会写入仓库里的 `00_每日信息差简报/`，然后你再通过 `git pull` 同步到本地 Obsidian。

问题：`.env` 会不会上传到 GitHub。

处理：不要手动添加 `.env`。项目的 `.gitignore` 已经包含：

```text
.env
__pycache__/
logs/
```

问题：想改每天运行时间。

处理：修改 `.github/workflows/daily-brief.yml` 里的 cron。记住 GitHub 使用 UTC 时间，北京时间要减去 8 小时。
