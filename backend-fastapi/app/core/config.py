from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str
    DB_NAME: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"  # 👈 Esto le dice a Pydantic que lea tu archivo .env

settings = Settings()
