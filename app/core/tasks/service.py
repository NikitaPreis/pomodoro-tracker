from dataclasses import dataclass

from app.exception import (TaskNotFoundException,
                           TaskStatusNotCorrect,
                           CategoryNotFoundException)
from app.core.categories.repository import CategoryRepository
from app.constants import TASK_STATUSES
from app.core.tasks.models import Task
from app.core.tasks.repository import TaskCache, TaskRepository
from app.core.tasks.schema import (TaskSchema, TaskCreateSchema,
                                   TaskUpdateSchema)
from app.core.tasks.utils import TaskFilter


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache
    category_repository: CategoryRepository

    async def get_tasks(self, user_id: int):
        tasks = await self.task_repository.get_tasks(user_id=user_id)
        return tasks

    async def get_filtered_tasks(
        self, user_id: int, task_filter: TaskFilter
    ):
        tasks = await self.task_repository.get_filtered_tasks(
            user_id=user_id, task_filter=task_filter
        )
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

    async def update_task(
        self, task_id: int, user_id: int, task: TaskUpdateSchema
    ):
        await self._check_task_status_correct(task_status=task.status)
        await self._check_users_task_exists(
            task_id=task_id, user_id=user_id
        )
        updated_task: Task = await self.task_repository.update_task(
            task_id=task_id, user_id=user_id, task=task
        )
        task_schema = TaskSchema.model_validate(updated_task)
        await self.task_cache.delete_task(task_id=task_id)
        return task_schema


    async def delete_task(self, task_id: int, user_id: int) -> None:
        await self._check_users_task_exists(
            task_id=task_id, user_id=user_id
        )
        await self.task_repository.delete_task(task_id=task_id, user_id=user_id)
        await self.task_cache.delete_task(task_id=task_id)

    async def update_task_name(
        self, task_id: int, name: str, user_id: int
    ) -> TaskSchema:
        await self._check_users_task_exists(
            task_id=task_id, user_id=user_id
        )
        updated_task = await self.task_repository.update_task_name(task_id=task_id, name=name)
        task_schema = TaskSchema.model_validate(updated_task)
        await self.task_cache.delete_task(task_id=task_id)
        return task_schema

    async def update_task_category(
        self, user_id: int, task_id: int, category_name: int
    ):
        await self._check_users_task_exists(
            task_id=task_id, user_id=user_id
        )
        category = await self.category_repository.get_category_by_name(
            user_id=user_id, category_name=category_name
        )
        if not category:
            raise CategoryNotFoundException
        updated_task = await self.task_repository.update_task_category(
            user_id=user_id, task_id=task_id, category_id=category.id
        )
        task_schema = TaskSchema.model_validate(updated_task)
        await self.task_cache.delete_task(task_id=task_id)
        return task_schema

    async def update_task_status(
        self, user_id: int, task_id: int, task_status: str
    ) -> TaskSchema:
        await self._check_task_status_correct(task_status=task_status)
        await self._check_users_task_exists(
            task_id=task_id, user_id=user_id
        )
        updated_task = await self.task_repository.update_task_status(
            user_id=user_id, task_id=task_id, task_status=task_status
        )
        task_schema = TaskSchema.model_validate(updated_task)
        await self.task_cache.delete_task(task_id=task_id)
        return task_schema

    async def _check_users_task_exists(
        self, task_id: int, user_id: int
    ) -> Task:
        task = await self.task_repository.get_user_task(
            user_id=user_id, task_id=task_id
        )
        if not task:
            raise TaskNotFoundException
        return task

    async def _check_task_status_correct(
        self, task_status: str
    ) -> None:
        if task_status not in TASK_STATUSES:
            raise TaskStatusNotCorrect

    # async def get_tasks_by_category(
    #     self, user_id: int, category_name: int,
    # ) -> list[TaskSchema]:
    #     category = await self.category_repository.get_category_by_name(
    #         category_name=category_name, user_id=user_id
    #     )
    #     if not category:
    #         raise CategoryNotFoundException
    #     tasks = await self.task_repository.get_tasks_by_category_name(
    #         user_id=user_id, category_name=category_name
    #     )
    #     if not tasks:
    #         raise TaskNotFoundException
    #     return [TaskSchema.model_validate(task) for task in tasks]
