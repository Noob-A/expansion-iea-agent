from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration."""
    database_url: str = "sqlite+aiosqlite:///./app.db"
    parser_concurrency: int = 4

    class Config:
        env_file = '.env'


settings = Settings()
