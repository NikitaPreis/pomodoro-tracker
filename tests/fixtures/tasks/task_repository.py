from dataclasses import dataclass

import pytest

from app.tasks.schema import TaskSchema, TaskCreateSchema
from tests.fixtures.tasks.task_schemas import get_task_schema
from tests.fixtures.tasks.task_model import (TaskFactory, get_task_id,
                                             get_task_name,
                                             get_task_category_id,
                                             get_task_pomodoro_count,
                                             get_task_user_id)


@dataclass
class FakeTaskRepository:

    async def get_tasks(self, user_id: int):
        task_1 = TaskFactory(
            user_id=user_id
        )
        task_2 = TaskFactory(
            user_id=user_id
        )
        return [task_1, task_2]

    async def get_task(self, task_id: int):
        return TaskFactory(
            id=task_id,
            name=get_task_name(),
            pomodoro_count=get_task_pomodoro_count(),
            category_id=get_task_category_id(),
            user_id=get_task_user_id()
        )

    async def get_user_task(self, task_id: int, user_id: int):
        return TaskFactory(id=task_id, user_id=user_id)

    async def create_task(self, task: TaskCreateSchema, user_id: int):
        return TaskFactory(id=get_task_id()).id

    async def update_task_name(self, task_id: int, name: str):
        return TaskFactory(
            id=task_id,
            name=name,
            user_id=get_task_user_id()
        )

@pytest.fixture
def task_repository():
    return FakeTaskRepository()
