from pydantic_settings import BaseSettings

"""
Configuration class for the app.
Precendences:
1. ENV Vars
2. .env File
3. Default Vars
"""

class AppSettings(BaseSettings):
    api_port: int | None = 8000

    class Config:
        env_file = ".env"