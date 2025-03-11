from dataclasses import dataclass

from app.exception import (TaskNotFoundException,
                           TaskStatusNotCorrect,
                           CategoryNotFoundException)
from app.core.categories.repository import CategoryRepository
from app.core.tasks.models import TaskStatusEnum
from app.core.tasks.repository import TaskCache, TaskRepository
from app.core.tasks.schema import TaskSchema, TaskCreateSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache
    category_repository: CategoryRepository

    async def get_tasks(self, user_id: int):
        tasks = await self.task_repository.get_tasks(user_id=user_id)
        return tasks

    async def get_task(self, task_id: int) -> TaskSchema:
        if task := await self.task_cache.get_task(task_id=task_id):
            print("Get from cache")
            return task
        if task := await self.task_repository.get_task(task_id=task_id):
            task_schema = TaskSchema.model_validate(task)
            print("Get from db")
            return task_schema
        raise TaskNotFoundException

    async def create_task(
            self, user_id: int, body: TaskCreateSchema
    ) -> TaskSchema:
        task_id = await self.task_repository.create_task(
            user_id=user_id, task=body
        )

        task = await self.task_repository.get_task(task_id=task_id)
        task_schema = TaskSchema.model_validate(task)

        await self.task_cache.set_task(
            task_id=task_schema.id,
            task=task_schema
        )
        return task_schema

    async def update_task_name(
            self, task_id: int, name: str, user_id: int
    ) -> TaskSchema:
        task = await self.task_repository.get_user_task(
            user_id=user_id, task_id=task_id
        )
        if not task:
            raise TaskNotFoundException
        task = await self.task_repository.update_task_name(task_id=task_id, name=name)
        task_schema = TaskSchema.model_validate(task)
        await self.task_cache.delete_task(task_id=task_id)
        return task_schema

    async def delete_task(self, task_id: int, user_id: int):
        task = await self.task_repository.get_user_task(
            task_id=task_id, user_id=user_id
        )
        if not task:
            raise TaskNotFoundException
        await self.task_repository.delete_task(task_id=task_id, user_id=user_id)
        await self.task_cache.delete_task(task_id=task_id)

    async def task_done(
        self, user_id: int, task_id
    ):
        pass

    async def update_task_category(
        self, user_id: int, task_id: int, category_name: int
    ):
        task = await self.task_repository.get_user_task(
            user_id=user_id, task_id=task_id
        )
        if not task:
            raise TaskNotFoundException
        category = await self.category_repository.get_category_by_name(
            user_id=user_id, category_name=category_name
        )
        if not category:
            raise CategoryNotFoundException
        updated_task = await self.task_repository.update_task_category(
            user_id=user_id, task_id=task_id, category_id=category.id
        )
        task_schema = TaskSchema.model_validate(updated_task)
        return task_schema

    async def get_tasks_by_category(
        self, user_id: int, category_name: int,
    ) -> list[TaskSchema]:
        category = await self.category_repository.get_category_by_name(
            category_name=category_name, user_id=user_id
        )
        if not category:
            raise CategoryNotFoundException
        tasks = await self.task_repository.get_tasks_by_category_name(
            user_id=user_id, category_name=category_name
        )
        if not tasks:
            raise TaskNotFoundException
        return [TaskSchema.model_validate(task) for task in tasks]

    async def update_task_status(
        self, user_id: int, task_id: int, task_status: str
    ) -> TaskSchema:
        task = await self.task_repository.get_task(task_id=task_id)
        if not task:
            raise TaskNotFoundException
        try:
            updated_task = await self.task_repository.update_task_status(
                user_id=user_id, task_id=task_id, task_status=task_status
            )
        except Exception as e:
            raise TaskStatusNotCorrect
        return TaskSchema.model_validate(updated_task)
