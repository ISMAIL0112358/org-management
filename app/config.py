from pydantic import BaseSettings

class Settings(BaseSettings):
    secret_key: str = "your_jwt_secret"

    class Config:
        env_file = ".env"

settings = Settings()
