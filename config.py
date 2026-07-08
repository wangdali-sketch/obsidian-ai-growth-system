"""
项目配置读取模块。

这个文件只负责读取 .env 里的配置，不负责生成简报。
"""

import os
from dataclasses import dataclass
from pathlib import Path


# 代码项目所在文件夹。.env 文件也放在这个目录里。
PROJECT_DIR = Path(__file__).resolve().parent


@dataclass
class AppConfig:
    """保存程序运行需要的配置。"""

    obsidian_vault_path: Path
    llm_provider: str
    llm_api_key: str
    llm_base_url: str
    llm_model: str


def load_dotenv_safely() -> None:
    """安全加载 .env 文件；没有安装 python-dotenv 时也能读取简单配置。"""
    env_path = PROJECT_DIR / ".env"

    try:
        from dotenv import load_dotenv
    except ImportError:
        load_simple_env_file(env_path)
        return

    load_dotenv(env_path)


def is_github_actions() -> bool:
    """判断当前是否运行在 GitHub Actions 云端环境。"""
    return os.getenv("GITHUB_ACTIONS", "").strip().lower() == "true"


def get_env_text(name: str, default: str = "") -> str:
    """读取文本环境变量；如果为空，就使用默认值。"""
    value = os.getenv(name, "").strip()
    if value:
        return value
    return default


def load_simple_env_file(env_path: Path) -> None:
    """读取简单的 .env 文件，格式为 KEY=VALUE。"""
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if key and key not in os.environ:
            os.environ[key] = value


def load_config() -> AppConfig:
    """从环境变量读取配置，并提供适合新手测试的默认值。"""
    running_in_github_actions = is_github_actions()

    # 本地运行才读取 .env；云端运行只读取 GitHub Secrets 注入的环境变量。
    if not running_in_github_actions:
        load_dotenv_safely()

    if running_in_github_actions:
        output_path = PROJECT_DIR
    else:
        vault_path_text = os.getenv("OBSIDIAN_VAULT_PATH", "").strip()
        if not vault_path_text:
            vault_path_text = str(PROJECT_DIR)
        output_path = Path(vault_path_text)

    return AppConfig(
        obsidian_vault_path=output_path,
        llm_provider=get_env_text("LLM_PROVIDER", "deepseek"),
        llm_api_key=get_env_text("LLM_API_KEY"),
        llm_base_url=get_env_text("LLM_BASE_URL", "https://api.deepseek.com"),
        llm_model=get_env_text("LLM_MODEL", "deepseek-v4-flash"),
    )
