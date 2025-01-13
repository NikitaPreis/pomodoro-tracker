from typing import Annotated

from fastapi import Depends

from cache import get_redis_connection
from database import get_db_session
from repository import TaskRepository, TaskCache
from service import TaskService


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_cache_tasks_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)


def get_task_service(
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
    task_cache: Annotated[TaskCache, Depends(get_cache_tasks_repository)]
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache
    )
