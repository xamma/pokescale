from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    api_port: int | None = 8000

    class Config:
        env_file = ".env"