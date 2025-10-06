from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class WordPressConfig(BaseSettings):
    WP_USERNAME: str
    WP_APP_PASSWORD: str
    WP_BASE_URL: str = Field(..., examples=['http://localhost:8000', 'https://example.com'])


class GoogleEnvConfig(BaseSettings):
    GEMINI_API_KEY: Optional[str] = Field(default=None, description='Gemini DeveloperのAPIキー')
    GOOGLE_GENAI_USE_VERTEXAI: bool = Field(default=False, description='Vertex AIを使用するかどうか')
    GOOGLE_CLOUD_PROJECT_ID: Optional[str] = Field(default=None, description='Google CloudのプロジェクトID')
    GOOGLE_CLOUD_LOCATION: str = Field(default='us-central1', description='Google Cloudのリージョン（デフォルト: us-central1）')


class EnvConfig(WordPressConfig, GoogleEnvConfig):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


env_config = EnvConfig()
