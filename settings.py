from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_DRIVER: str = 'postgresql+psycopg2'
    DB_PASSWORD: str = 'mysecretpassword'
    DB_USER: str = 'postgres_user'
    DB_NAME: str = 'pomodoro'
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    CACHE_HOST: str = '127.0.0.1'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    JWT_SECRET_KEY: str = 'secret_key'
    JWT_ENCODE_ALHORITHM: str = 'HS256'


    @property
    def db_url(self):
        return (f'{self.DB_DRIVER}://{self.DB_USER}:'
                f'{self.DB_PASSWORD}@{self.DB_HOST}:'
                f'{self.DB_PORT}/{self.DB_NAME}')

settings = Settings()
