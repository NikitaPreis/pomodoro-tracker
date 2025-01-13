from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLITE_DB_NAME: str = 'db.sqlite3'
    POSTGRES_PASSWORD: str = 'postgrespassword'
    POSTGRES_USER: str = 'postgres_user'
    POSTGRES_DB: str = 'postgres_db'
    POSTGRES_HOST: str = 'local_host'
    POSTGRES_PORT: str = '5432'

settings = Settings()
