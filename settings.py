from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DRIVER: str = 'postgresql+psycopg2'
    POSTGRES_PASSWORD: str = 'mysecretpassword'
    POSTGRES_USER: str = 'postgres_user'
    POSTGRES_DB: str = 'pomodoro'
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432

    DB_DRIVER: str = 'postgresql+psycopg2'
    DB_PASSWORD: str = 'mysecretpassword'
    DB_USER: str = 'postgres_user'
    DB_NAME: str = 'postgres_db'
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    CACHE_HOST: str = '0.0.0.0'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0

    @property
    def db_url(self):
        return (f'{self.DB_DRIVER}://{self.DB_USER}:'
                f'{self.DB_PASSWORD}@{self.DB_HOST}:'
                f'{self.DB_PORT}/{self.DB_NAME}')

settings = Settings()
