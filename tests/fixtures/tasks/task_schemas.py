import pytest

from app.tasks.schema import TaskSchema, TaskCreateSchema

id: int | None = None 
name: str | None = None
pomodoro_count: int | None = None
category_id: int
user_id: int

def get_task_id():
    return 123


def get_task_name():
    return 'test_name'


def get_task_pomodoro_count():
    return 10


def get_task_category_id():
    return 456


def get_task_user_id():
    return 567


def get_updated_name():
    return 'updated_name'


@pytest.fixture
def updated_name():
    return get_updated_name()


def get_task_schema():
    return TaskSchema(
        id=get_task_id(),
        name=get_task_name(),
        pomodoro_count=get_task_pomodoro_count(),
        category_id=get_task_category_id(),
        user_id=get_task_user_id()
    )


@pytest.fixture
def task_schema():
    return get_task_schema()
