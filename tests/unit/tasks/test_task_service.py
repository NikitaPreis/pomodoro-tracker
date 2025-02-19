import pytest

from app.tasks.service import TaskService
from app.tasks.schema import TaskSchema, TaskCreateSchema
from app.tasks.models import Task
from tests.fixtures.tasks.task_model import (TaskFactory, get_task_id,
                                             get_task_name,
                                             get_task_category_id,
                                             get_task_pomodoro_count,
                                             get_task_user_id)

class TestTaskService:

    async def test_get_tasks_success(
        self, task_service: TaskService
    ):
        user_id = get_task_user_id()
        tasks = await task_service.get_tasks(user_id=user_id)

        for task in tasks:
            assert isinstance(task, Task)
            assert task.user_id == user_id

    async def test_get_task_success(
        self, task_service: TaskService
    ):
        task_id = get_task_id()
        task = await task_service.get_task(task_id=task_id)

        assert isinstance(task, TaskSchema)
        assert task.id == task_id

    async def test_create_task_success(
        self, task_service: TaskService
    ):
        task_id = get_task_id()
        user_id = get_task_user_id()
        task_name = get_task_name()
        task_pomodoro_count = get_task_pomodoro_count()
        task_category_id = get_task_category_id()

        create_user_schema = TaskCreateSchema(
            name=task_name,
            pomodoro_count=task_pomodoro_count,
            category_id=task_category_id
        )

        task = await task_service.create_task(
            user_id=user_id, body=create_user_schema
        )

        assert isinstance(task, TaskSchema)
        assert task.id == task_id
        assert task.name == task_name
        assert task.pomodoro_count == task_pomodoro_count
        assert task.category_id == task_category_id

    async def test_update_task_name(
        self, task_service: TaskService, task_schema: TaskSchema,
        updated_name
    ):

        task = await task_service.update_task_name(
            task_id=task_schema.id,
            name=updated_name,
            user_id=task_schema.user_id
        )

        assert isinstance(task, TaskSchema)
        assert task.id == task_schema.id
        assert task.name == updated_name
        assert task.user_id == task_schema.user_id
