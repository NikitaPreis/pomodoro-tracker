from dataclasses import dataclass

import pytest

from app.tasks.schema import TaskSchema, TaskCreateSchema
from tests.fixtures.users.user_model import UserProfileFactory, get_fake_password, get_fake_user_id


@dataclass
class FakeTaskCache:


    async def get_task(self, task_id: int):
        return None

    async def set_task(self, task_id: int, task: TaskSchema):
        return None

    async def delete_task(self, task_id: int):
        return None

    def _create_key_by_task_id(self, task_id: int) -> str:
        return f'task_{task_id}'



@pytest.fixture
def task_cache():
    return FakeTaskCache()
