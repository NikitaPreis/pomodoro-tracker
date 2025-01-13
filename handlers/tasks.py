from typing import Annotated

from fastapi import APIRouter, Depends, status

from dependecy import get_task_service, get_cache_tasks_repository, get_tasks_repository
from repository import TaskRepository, TaskCache
from service import TaskService
from schema.tasks import TaskSchema


router = APIRouter(
    prefix='/tasks',
    tags=['tasks']
)


@router.get(
        path='/',
        response_model=list[TaskSchema]
)
async def get_tasks(
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
):
    tasks = task_repository.get_tasks()
    return tasks


@router.get(
        path='/{task_id}',
        response_model=TaskSchema
)
async def get_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)]
):
    return task_service.get_task(task_id=task_id)


@router.post(
        '/',
        response_model=TaskSchema
)
async def create_task(
    task: TaskSchema,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
) -> TaskSchema:
    task_id = task_repository.create_task(task)
    task.id = task_id
    return task


@router.patch(
        '/{task_id}',
        response_model=TaskSchema,
        status_code=status.HTTP_201_CREATED
)
async def update_task_name(
    task_id: int, name: str,
    task_serice: Annotated[TaskService, Depends(get_task_service)]
) -> TaskSchema:
    return task_serice.update_task_name(task_id=task_id, name=name)


@router.delete(
        '/{task_id}',
        status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)]
):
    return task_service.delete_task(task_id=task_id)
