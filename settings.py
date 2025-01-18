from pydantic_settings import BaseSettings


# class Settings(BaseSettings):
#     POSTGRES_DRIVER: str = 'postgresql+psycopg2'
#     POSTGRES_PASSWORD: str = 'mysecretpassword'
#     POSTGRES_USER: str = 'postgres_user'
#     POSTGRES_DB: str = 'pomodoro'
#     POSTGRES_HOST: str = 'localhost'
#     POSTGRES_PORT: int = 5432

#     DB_DRIVER: str = 'postgresql+psycopg2'
#     DB_PASSWORD: str = 'mysecretpassword'
#     DB_USER: str = 'postgres_user'
#     DB_NAME: str = 'pomodoro'
#     DB_HOST: str = '0.0.0.0'
#     DB_PORT: int = 5432

#     CACHE_HOST: str = '127.0.0.1'
#     CACHE_PORT: int = 6379
#     CACHE_DB: int = 0
#     JWT_SECRET_KEY: str = 'secret_key'
#     JWT_ENCODE_ALHORITHM: str = 'HS256'
#     GOOGLE_CLIENT_ID: str = ''
#     GOOGLE_CLIENT_SECRET: str = ''
#     GOOGLE_REDIRECT_URI: str = ''
#     GOOGLE_TOKEN_URL: str = 'https://accounts.google.com/o/oauth2/token'


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
    GOOGLE_CLIENT_ID: str = ''
    GOOGLE_CLIENT_SECRET: str = ''
    GOOGLE_REDIRECT_URI: str = ''
    GOOGLE_TOKEN_URL: str = 'https://accounts.google.com/o/oauth2/token'


    @property
    def db_url(self):
        return (f'{self.DB_DRIVER}://{self.DB_USER}:'
                f'{self.DB_PASSWORD}@{self.DB_HOST}:'
                f'{self.DB_PORT}/{self.DB_NAME}')


    @property
    def google_redirect_url(self) -> str:
        return (f'https://accounts.google.com/o/oauth2/auth'
                f'?response_type=code&client_id={self.GOOGLE_CLIENT_ID}'
                f'&redirect_uri={self.GOOGLE_REDIRECT_URI}'
                f'&scope=openid%20profile%20email&access_type=offline')

settings = Settings()
