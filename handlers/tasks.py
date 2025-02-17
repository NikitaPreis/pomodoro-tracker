from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from exception import TaskNotFoundException, UserNotFoundException
from dependecy import get_task_service, get_cache_tasks_repository, get_tasks_repository, get_request_user_id
from repository import TaskRepository, TaskCache
from service import TaskService
from schema.tasks import TaskSchema, TaskCreateSchema


router = APIRouter(
    prefix='/tasks',
    tags=['tasks']
)


@router.get(
        path='/',
        response_model=list[TaskSchema]
)
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
):
    tasks = await task_service.get_tasks(user_id=user_id)
    return tasks


@router.get(
        path='/{task_id}',
        response_model=TaskSchema
)
async def get_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
):
    try:
        return await task_service.get_task(
            task_id=task_id
        )
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )


@router.post(
        '/',
        response_model=TaskSchema
)
async def create_task(
    body: TaskCreateSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
) -> TaskSchema:
    task = await task_service.create_task(body=body, user_id=user_id)
    return task


@router.patch(
        '/{task_id}',
        response_model=TaskSchema,
        status_code=status.HTTP_201_CREATED
)
async def update_task_name(
    task_id: int, name: str,
    task_serice: Annotated[TaskService, Depends(get_task_service)],
    user_id:int = Depends(get_request_user_id)
) -> TaskSchema:
    try:
        task = await task_serice.update_task_name(
           task_id=task_id, name=name, user_id=user_id
        )
        return task
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )


@router.delete(
        '/{task_id}',
        status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id:int = Depends(get_request_user_id)
):
    try:
        return await task_service.delete_task(
            task_id=task_id, user_id=user_id
        )
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )
