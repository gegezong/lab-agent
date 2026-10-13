from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # 后端项目的根路径


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_EXPIRE_HOURS: int = 24
    JWT_ALGORITHM: str = "HS256"
    LLM_API_KEY: str
    LLM_BASE_URL: str
    LLM_MODEL: str
    KB_EMBEDDING_MODEL: str = "BAAI/bge-small-zh-v1.5"
    KB_EMBEDDING_LOCAL_FILES_ONLY: bool = True
    KB_WARMUP_ON_STARTUP: bool = False

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8"
    )


settings = Settings()

UPLOAD_DIR = BASE_DIR / "uploads"  # 上传文件的保存路径
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # 如果不存在则创建上传目录
MAX_FILE_SIZE = 1024 * 1024 * 100  # 最大文件大小，100MB


# 文件上传后缀限制
ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".zip",
}
