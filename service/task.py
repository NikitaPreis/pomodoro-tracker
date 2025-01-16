from dataclasses import dataclass

from exception import TaskNotFoundException
from repository import TaskCache, TaskRepository
from schema.tasks import TaskSchema, TaskCreateSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    # def get_task(self, task_id) -> TaskSchema:
    #     if task := self.task_cache.get_task(task_id=task_id):
    #         return task
    #     task = self.task_repository.get_task(task_id=task_id)
    #     task_schema = TaskSchema.model_validate(task)
    #     self.task_cache.set_task(task_id=task.id, task=task_schema)
    #     return task

    def get_tasks(self, user_id: int):
        tasks = self.task_repository.get_tasks(user_id=user_id)
        return tasks

    def get_task(self, task_id: int, user_id: int) -> TaskSchema:
        task = self.task_repository.get_user_task(
            task_id=task_id, user_id=user_id
        )
        if not task:
            raise TaskNotFoundException
        return TaskSchema.model_validate(task)

    def create_task(
            self, user_id: int, body: TaskCreateSchema
    ) -> TaskSchema:
        task_id = self.task_repository.create_task(
            user_id=user_id, task=body
        )
        task = self.task_repository.get_task(task_id=task_id)
        return TaskSchema.model_validate(task)

    def update_task_name(
            self, task_id: int, name: str, user_id: int
    ) -> TaskSchema:
        task = self.task_repository.get_user_task(
            user_id=user_id, task_id=task_id
        )
        if not task:
            raise TaskNotFoundException
        task = self.task_repository.update_task_name(task_id=task_id, name=name)
        self.task_cache.delete_task(task_id=task_id)
        return TaskSchema.model_validate(task)

    def delete_task(self, task_id: int, user_id: int):
        task = self.task_repository.get_user_task(
            task_id=task_id, user_id=user_id
        )
        if not task:
            raise TaskNotFoundException
        self.task_repository.delete_task(task_id=task_id, user_id=user_id)
        self.task_cache.delete_task(task_id=task_id)
