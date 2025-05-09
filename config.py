from pydantic import BaseSettings, Field, ValidationError

class Settings(BaseSettings):
    telegram_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")
    manager_id: int = Field(..., env="MANAGER_ID")
    bot_username: str = Field(..., env="BOT_USERNAME")

    class Config:
        env_file = ".env"

try:
    settings = Settings()
except ValidationError as e:
    print("Configuration error:", e)
    raise SystemExit(1)
