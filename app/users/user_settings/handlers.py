from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from app.dependecy import get_request_user_id, get_user_settings_service
from app.exception import UserSettingsNotFoundException
from app.users.user_settings.service import UserSettingsService
from app.users.user_settings.schema import UserSettingsSchema


router = APIRouter(
    prefix='/settings',
    tags=['settings']
)


@router.get(
    path='/',
    response_model=UserSettingsSchema,
    status_code=status.HTTP_200_OK,
)
async def get_user_settings(
    user_settings_service: Annotated[
        UserSettingsService, Depends(get_user_settings_service)
    ],
    user_id: int = Depends(get_request_user_id)
) -> UserSettingsSchema:
    """Get all user settings."""
    try:
        return await user_settings_service.get_user_settings(user_id=user_id)
    except UserSettingsNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.put(
    path='/default',
    response_model=UserSettingsSchema,
    status_code=status.HTTP_201_CREATED
)
async def reset_settings(
    user_settings_service: Annotated[
        UserSettingsService, Depends(get_user_settings_service)
    ],
    user_id: int = Depends(get_request_user_id)
):
    """Reset user settings to default."""
    try:
        return await user_settings_service.reset_settings(user_id=user_id)
    except UserSettingsNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.patch(
    path='/pomodoro-duration',
    response_model=UserSettingsSchema,
    status_code=status.HTTP_201_CREATED
)
async def update_pomodoro_duration(
    pomodoro_duration: int,
    user_settings_service: Annotated[
        UserSettingsService, Depends(get_user_settings_service)
    ],
    user_id: int = Depends(get_request_user_id)
):
    """Set duration of pomodoros in minutes (int)."""
    try:
        return await user_settings_service.set_pomodoro_duration(
            user_id=user_id, pomodoro_duration=pomodoro_duration
        )
    except UserSettingsNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.patch(
    path='/short-break-duration',
    response_model=UserSettingsSchema,
    status_code=status.HTTP_201_CREATED
)
async def update_short_break_duration(
    short_break_duration: int,
    user_settings_service: Annotated[
        UserSettingsService, Depends(get_user_settings_service)
    ],
    user_id: int = Depends(get_request_user_id)
):
    """Set duration of short breaks between pomodoros in minutes."""
    try:
        return await user_settings_service.set_pomodoro_short_break_duration(
            user_id=user_id, short_break_duration=short_break_duration
        )
    except UserSettingsNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.patch(
    path='/long-break-duration',
    response_model=UserSettingsSchema,
    status_code=status.HTTP_201_CREATED
)
async def update_long_break_duration(
    long_break_duration: int,
    user_settings_service: Annotated[
        UserSettingsService, Depends(get_user_settings_service)
    ],
    user_id: int = Depends(get_request_user_id)
):
    """Set duration of long breaks between pomodoros in minutes."""
    try:
        return await user_settings_service.set_pomodoro_long_break_duration(
            user_id=user_id, long_break_duration=long_break_duration
        )
    except UserSettingsNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.patch(
    path='/long-break-interval',
    response_model=UserSettingsSchema,
    status_code=status.HTTP_201_CREATED
)
async def update_long_break_interval(
    long_break_interval: int,
    user_settings_service: Annotated[
        UserSettingsService, Depends(get_user_settings_service)
    ],
    user_id: int = Depends(get_request_user_id)
):
    """Set interval between long breaks."""

    try:
        return await user_settings_service.set_interval_between_long_breaks(
            user_id=user_id, long_break_interval=long_break_interval
        )
    except UserSettingsNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
