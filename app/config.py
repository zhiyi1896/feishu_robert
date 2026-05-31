from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8")

    app_env: str = Field(default="local", alias="APP_ENV")
    database_url: str = Field(default="mysql+asyncmy://root:password@localhost:3306/feishu_task_bot?charset=utf8mb4", alias="DATABASE_URL")
    feishu_app_id: str = Field(default="", alias="FEISHU_APP_ID")
    feishu_app_secret: str = Field(default="", alias="FEISHU_APP_SECRET")
    feishu_verification_token: str = Field(default="", alias="FEISHU_VERIFICATION_TOKEN")
    feishu_encrypt_key: str = Field(default="", alias="FEISHU_ENCRYPT_KEY")
    #日志
    log_file_enable: bool = Field(default=True, alias="LOG_FILE_ENABLE")
    log_file_level: str = Field(default="INFO", alias="LOG_FILE_LEVEL")
    log_file_path: str = Field(default="logs", alias="LOG_FILE_PATH")
    log_file_rotation: str = Field(default="10MB", alias="LOG_FILE_ROTATION")
    log_file_retention: str = Field(default="7 days", alias="LOG_FILE_RETENTION")

    # 日志配置 - 控制台日志
    log_console_enable: bool = Field(default=True, alias="LOG_CONSOLE_ENABLE")
    log_console_level: str = Field(default="INFO", alias="LOG_CONSOLE_LEVEL")

    #LLM配置
    api_key: str = Field(default="", alias="OPENAI_API_KEY")
    llm_url: str = Field(default="", alias="OPENAI_BASE_URL")

    api_key2: str = Field(default="", alias="OPENAI_API_KEY2")
    llm_url2: str = Field(default="", alias="OPENAI_BASE_URL2")


@lru_cache
def get_settings() -> Settings:
    return Settings()