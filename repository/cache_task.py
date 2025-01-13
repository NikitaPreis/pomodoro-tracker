import json

from redis import Redis

from schema.tasks import TaskSchema

class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_task(self, task_id: int):
        task_key = self.create_key_by_task_id(task_id)
        with self.redis as redis:
            task_json = redis.get(task_key)
        if task_json:
            return TaskSchema.model_validate(json.loads(task_json))
        return None

    def set_task(self, task_id: int, task: TaskSchema):
        task_json = task.model_dump_json()
        task_key = self.create_key_by_task_id(task_id=task_id)
        with self.redis as redis:
            redis.setex(task_key, 60*60, task_json)

    def delete_task(self, task_id: int):
        with self.redis as redis:
            redis.delete(f'task_{task_id}')

    def create_key_by_task_id(self, task_id: int) -> str:
        return f'task_{task_id}'
    

    def get_tasks(self):
        pass

    def set_tasks(self, tasks: list[TaskSchema]):
        pass
        # tasks_json = [task.json() for task in tasks]
        # self.redis.lpush('tasks', *tasks_json)
