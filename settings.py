from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_PASSWORD: str = 'mysecretpassword'
    POSTGRES_USER: str = 'postgres_user'
    POSTGRES_DB: str = 'postgres_db'
    POSTGRES_HOST: str = '0.0.0.0'
    POSTGRES_PORT: int = 5432
    CACHE_HOST: str = '0.0.0.0'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0

settings = Settings()
