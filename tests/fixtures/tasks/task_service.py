import pytest

from app.tasks.service import TaskService


@pytest.fixture
def task_service(task_repository, task_cache):
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache
    )
