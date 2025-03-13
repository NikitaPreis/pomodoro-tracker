from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException

from app.core.categories.schema import CategoryCreateSchema, CategorySchema
from app.core.categories.service import CategoryService
from app.dependecy import get_category_service, get_request_user_id
from app.exception import (CategoryNotFoundException, UserNotFoundException,
                           UsersCategoryNameShouldBeUniqueException)


router = APIRouter(prefix='/categories', tags=['categories'])


@router.get(
    path='/',
    response_model=list[CategorySchema],
    status_code=status.HTTP_200_OK
)
async def get_categories(
    category_service: Annotated[
        CategoryService, Depends(get_category_service)
    ],
    user_id: int = Depends(get_request_user_id)
):
    """Retrieves all user categories."""
    return await category_service.get_categories(
        user_id=user_id
    ) 


@router.post(
    path='/',
    response_model=CategorySchema,
    status_code=status.HTTP_201_CREATED
)
async def create_category(
    body: CategoryCreateSchema,
    category_service: Annotated[
        CategoryService, Depends(get_category_service)
    ],
    user_id: int = Depends(get_request_user_id),
):
    """Create user category."""
    try:
        return await category_service.create_category(
            user_id=user_id, body=body
        )
    except UsersCategoryNameShouldBeUniqueException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.detail
        )


@router.put(
    path='/{category_id}',
    response_model=CategorySchema,
    status_code=status.HTTP_201_CREATED
)
async def update_category(
    category_id: int,
    body: CategoryCreateSchema,
    category_service: Annotated[
        CategoryService, Depends(get_category_service)
    ],
    user_id: int = Depends(get_request_user_id),
):
    """Update user category."""
    try:
        return await category_service.update_category(
            user_id=user_id, category_id=category_id,
            body=body
        )
    except CategoryNotFoundException as e:
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
    path='/{category_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_category(
    category_id: int,
    category_service: Annotated[
        CategoryService, Depends(get_category_service)
    ],
    user_id: int = Depends(get_request_user_id),
):
    """Delete user category."""
    try:
        return await category_service.delete_category(
            user_id=user_id, category_id=category_id
        )
    except CategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )
