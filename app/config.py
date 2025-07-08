from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    master_db_name: str
    master_db_user: str
    master_db_password: str
    master_db_host: str
    master_db_port: str

    class Config:
        env_file = ".env"

settings = Settings()
