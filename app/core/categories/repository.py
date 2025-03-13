from dataclasses import dataclass

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.categories.models import Category
from app.core.categories.schema import CategoryCreateSchema


@dataclass
class CategoryRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_categories(self, user_id: int) -> list[Category]:
        query = select(Category).where(Category.user_id == user_id)
        async with self.db_session as session:
            categories: list[Category] = (await session.execute(
                query
            )).scalars().all()
        return categories

    async def get_category(
        self, user_id: int, category_id: int
    ) -> Category | None:
        query = select(Category).where(
            Category.id == category_id, Category.user_id == user_id
        )
        async with self.db_session as session:
            category = (await session.execute(
                query
            )).scalar_one_or_none()
        return category

    async def get_category_by_name(
        self, user_id: int, category_name: str,
    ) -> Category | None:
        query = select(Category).where(
            Category.name == category_name, Category.user_id == user_id
        )
        async with self.db_session as session:
            category = (await session.execute(query)).scalar_one_or_none()
        return category

    async def create_category(
        self, user_id: int, category: CategoryCreateSchema
    ) -> int:
        statement = insert(Category).values(
            name=category.name,
            description=category.description,
            user_id=user_id,
        ).returning(Category.id)
        async with self.db_session as session:
            category_id = (await session.execute(
                statement
            )).scalar_one()
            await session.commit()
        return category_id

    async def update_category(
        self, category_id: int,
        category: CategoryCreateSchema
    ) -> Category:
        statement = update(Category).where(
            Category.id == category_id
        ).values(
            name=category.name,
            description=category.description
        ).returning(Category.id, Category.user_id)
        async with self.db_session as session:
            category_id, user_id = (await session.execute(
                statement
            )).one()
            await session.commit()
            return await self.get_category(
                category_id=category_id, user_id=user_id
            )

    async def delete_category(
        self, user_id: int, category_id: int
    ) -> None:
        statement = delete(Category).where(
            Category.id == category_id,
            Category.user_id == user_id
        )
        async with self.db_session as session:
            await session.execute(statement)
            await session.commit()
