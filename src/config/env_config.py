from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvConfig(BaseSettings):
    WP_USERNAME: str
    WP_APP_PASSWORD: str
    WP_BASE_URL: str = Field(..., examples=['http://localhost:8000', 'https://example.com'])

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


env_config = EnvConfig()
