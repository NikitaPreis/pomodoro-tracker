from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from app.dependecy import get_auth_service
from app.exception import (UserNotFoundException,
                           UserNotCorrectPasswordException,
                           UserSettingsCreatingException)
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.schema import UserCreateSchema
from app.users.auth.service import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/login',
    response_model=UserLoginSchema
)
async def login(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        return await auth_service.login(body.username, body.password)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
    except UserNotCorrectPasswordException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
    except UserSettingsCreatingException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )


@router.get(
    '/login/google',
    response_class=RedirectResponse,
    status_code=200
)
async def google_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> RedirectResponse:
    redirect_url: str = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get(
    '/google',
    response_model=UserLoginSchema
)
async def google_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str
) -> UserLoginSchema:
    try:
        return await auth_service.google_auth(code=code)
    except UserSettingsCreatingException as e:
            raise HTTPException(
                status_code=404,
                detail=e.detail
            )


@router.get(
    '/login/yandex',
    response_class=RedirectResponse
)
async def yandex_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url = auth_service.get_yandex_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get(
    '/yandex'
)
async def yandex_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str
):
    try:
        return await auth_service.yandex_auth(code=code)
    except UserSettingsCreatingException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
