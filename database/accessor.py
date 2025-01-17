from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings


# engine = create_engine(settings.db_url)


engine = create_engine(
    f'postgresql+psycopg2://{settings.POSTGRES_USER}:'
    f'{settings.POSTGRES_PASSWORD}@localhost:'
    f'{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}'
)


Session = sessionmaker(engine)


def get_db_session():
    return Session
