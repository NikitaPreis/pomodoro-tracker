from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError

from app.core.categories.repository import CategoryRepository
from app.core.categories.schema import CategorySchema, CategoryCreateSchema
from app.exception import (CategoryNotFoundException,
                           UsersCategoryNameShouldBeUniqueException)


@dataclass
class CategoryService:
    category_repository: CategoryRepository

    async def get_categories(
        self, user_id
    ) -> list[CategorySchema]:
        categories = await self.category_repository.get_categories(
            user_id=user_id
        )
        category_schemas = [CategorySchema.model_validate(category) for category in categories]
        return category_schemas

    async def create_category(
        self, user_id: int, body: CategoryCreateSchema
    ) -> CategorySchema:
        try:
            category_id = await self.category_repository.create_category(
                user_id=user_id, category=body
            )
        except IntegrityError as e:
            raise UsersCategoryNameShouldBeUniqueException
        category = await self.category_repository.get_category(
            user_id=user_id, category_id=category_id
        )
        category_schema = CategorySchema.model_validate(category)
        return category_schema

    async def update_category(
        self, user_id: int, category_id: int, body: CategoryCreateSchema
    ) -> CategorySchema:
        category = await self.category_repository.get_category(
            user_id=user_id, category_id=category_id
        )
        if not category:
            raise CategoryNotFoundException
        updated_category = await self.category_repository.update_category(
            category_id=category_id, category=body
        )
        category_schema = CategorySchema.model_validate(updated_category)
        return category_schema


    async def delete_category(
        self, user_id: int, category_id: int
    ) -> None:
        category = await self.category_repository.get_category(
            user_id=user_id, category_id=category_id
        )
        if not category:
            raise CategoryNotFoundException
        await self.category_repository.delete_category(
            user_id=user_id, category_id=category_id
        )
