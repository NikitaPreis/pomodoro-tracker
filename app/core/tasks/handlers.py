from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_filter import FilterDepends

from app.exception import (TaskNotFoundException, UserNotFoundException,
                           CategoryNotFoundException, TaskStatusNotCorrect)
from app.dependecy import get_task_service, get_request_user_id
from app.core.tasks.service import TaskService
from app.core.tasks.schema import (TaskSchema, TaskCreateSchema,
                                   TaskUpdateSchema)
from app.core.tasks.utils import TaskFilter


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
    task_filter: TaskFilter = FilterDepends(TaskFilter),
    user_id: int = Depends(get_request_user_id),
) -> list[TaskSchema]:
    try:
        return await task_service.get_filtered_tasks(
            user_id=user_id, task_filter=task_filter
        )
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


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


@router.put(
    '/{task_id}',
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED
)
async def update_task(
    task_id: int, body: TaskUpdateSchema,
    task_serice: Annotated[TaskService, Depends(get_task_service)],
    user_id:int = Depends(get_request_user_id)
) -> TaskSchema:
    try:
        return await task_serice.update_task(
           task_id=task_id, user_id=user_id, task=body
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


@router.patch(
    '/{task_id}/set-name',
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED
)
async def update_task_name(
    task_id: int, name: str,
    task_serice: Annotated[TaskService, Depends(get_task_service)],
    user_id:int = Depends(get_request_user_id)
) -> TaskSchema:
    try:
        return await task_serice.update_task_name(
           task_id=task_id, name=name, user_id=user_id
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


@router.patch(
    '/{task_id}/set-category',
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED
)
async def update_task_category(
    task_id: int, category_name: str,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id:int = Depends(get_request_user_id)
) -> TaskSchema:
    try:
        return await task_service.update_task_category(
            user_id=user_id, task_id=task_id, category_name=category_name
        )
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except CategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.patch(
    '/{task_id}/set-status',
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED
)
async def update_task_status(
    task_id: int, task_status: str,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id:int = Depends(get_request_user_id)
) -> TaskSchema:
    try:
        return await task_service.update_task_status(
            user_id=user_id, task_id=task_id, task_status=task_status
        )
    except TaskStatusNotCorrect as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.detail
        )
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
