from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.infrastructure.database.database import Base
from app.settings import settings


engine = create_async_engine(
    url=settings.db_url,
    future=True,
    echo=True,
    pool_pre_ping=True
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)

async def get_db_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session


async def init_models():
    from app.users.user_settings.models import UserSettings
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
