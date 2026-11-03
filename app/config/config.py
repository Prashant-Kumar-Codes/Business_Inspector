import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_FILES_DIR = BASE_DIR / 'static'
ENV_FILE = BASE_DIR / '.env'


class Config(BaseSettings):
    SECRET_KEY: str
    DB_URL: str
    AI_KEY: str

    MAIL_SERVER: str
    MAIL_PORT: int = 587
    MAIL_USE_TLS: bool = True
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_DEFAULT_SENDER: str
    
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding='utf-8',
        case_sesitive=True,
        extra='ignore'
    )

# create configuration instace
settings = Config()
        