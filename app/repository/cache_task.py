import json

from redis import asyncio as Redis

from app.schema.tasks import TaskSchema

class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_task(self, task_id: int):
        task_key = self._create_key_by_task_id(task_id)
        async with self.redis as redis:
            task_json = await redis.get(task_key)
        if task_json:
            return TaskSchema.model_validate(json.loads(task_json))
        return None

    async def set_task(self, task_id: int, task: TaskSchema):
        task_json = task.model_dump_json()
        task_key = self._create_key_by_task_id(task_id=task_id)
        async with self.redis as redis:
            await redis.setex(task_key, 60*60, task_json)

    async def delete_task(self, task_id: int):
        async with self.redis as redis:
            await redis.delete(f'task_{task_id}')

    def _create_key_by_task_id(self, task_id: int) -> str:
        return f'task_{task_id}'

    async def get_tasks(self):
        pass

    async def set_tasks(self, tasks: list[TaskSchema]):
        pass
