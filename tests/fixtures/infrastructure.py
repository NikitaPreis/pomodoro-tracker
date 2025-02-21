from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.infrastructure.database.database import Base
from app.settings import Settings


@pytest.fixture
def settings():
    return Settings()


test_engine = create_async_engine(
    url=Settings().db_url,
    future=True,
    echo=True,
    pool_pre_ping=True
)

AsyncSessionFactory = async_sessionmaker(
    test_engine,
    expire_on_commit=False,
    class_=AsyncSession
)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def init_models():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield test_engine
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope='function')
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            for table in reversed(Base.metadata.sorted_tables):
                await session.execute(text(f"TRUNCATE {table.name} CASCADE;"))
                await session.commit()
