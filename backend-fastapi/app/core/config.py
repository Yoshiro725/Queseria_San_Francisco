from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_url: str = "mongodb://127.0.0.1:27017"
    mongo_db: str = "Queseria_SanFrancisco"
    # Puedes agregar JWT o más configuraciones si lo necesitas
    jwt_secret_key: str = "supersecretkey"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

settings = Settings()
