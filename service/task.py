from dataclasses import dataclass

from exception import TaskNotFoundException
from repository import TaskCache, TaskRepository
from schema.tasks import TaskSchema, TaskCreateSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

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
