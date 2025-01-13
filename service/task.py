from dataclasses import dataclass

from repository import TaskCache, TaskRepository
from schema.tasks import TaskSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    def get_task(self, task_id) -> TaskSchema:
        if task := self.task_cache.get_task(task_id=task_id):
            print('from redis')
            return task
        task = self.task_repository.get_task(task_id=task_id)
        task_schema = TaskSchema.model_validate(task)
        self.task_cache.set_task(task_id=task.id, task=task_schema)
        return task

    def update_task_name(self, task_id, name) -> TaskSchema:
        task = self.task_repository.update_task_name(task_id=task_id, name=name)
        self.task_cache.delete_task(task_id=task_id)
        return task

    def delete_task(self, task_id):
        self.task_repository.delete_task(task_id=task_id)
        self.task_cache.delete_task(task_id=task_id)
