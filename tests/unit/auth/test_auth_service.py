import datetime as dt

import pytest
from jose import jwt
from unittest.mock import patch, Mock

from app.dependecy import get_auth_service
from app.exception import (UserNotFoundException,
                           UserNotCorrectPasswordException)
from app.settings import Settings
from app.users.auth.clients import GoogleClient
from tests.fixtures.users.user_model import UserProfileFactory, get_fake_password
from app.users.auth.service import AuthService
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.models import UserProfile


pytestmark = pytest.mark.asyncio


class TestAuthService:

    async def test_get_google_redirect_url_success(
        self, auth_service: AuthService, settings: Settings
    ):
        settings_google_redirect_url = settings.google_redirect_url
        auth_service_google_redirect_url = auth_service.get_google_redirect_url()
        assert settings_google_redirect_url == auth_service_google_redirect_url

    async def test_get_yandex_redirect_url_success(
        self, auth_service: AuthService, settings: Settings
    ):
        settings_yandex_redirect_url = settings.yandex_redirect_url
        auth_service_yandex_redirect_url = auth_service.get_yandex_redirect_url()
        assert settings_yandex_redirect_url == auth_service_yandex_redirect_url

    async def test_generate_access_token_success(
        self, auth_service: AuthService, settings: Settings
    ):
        user_id = str(1)
        access_token = auth_service.generate_access_token(
            user_id=user_id
        )

        decoded_access_token = jwt.decode(
            access_token, settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ENCODE_ALHORITHM]
        )
        decoded_user_id = decoded_access_token.get('user_id')
        decoded_token_expire = dt.datetime.fromtimestamp(
            decoded_access_token.get('expire'), tz=dt.timezone.utc
        )

        assert decoded_user_id == user_id
        assert (decoded_token_expire - dt.datetime.now(tz=dt.UTC) > dt.timedelta(days=6))

    async def test_get_user_id_from_access_token_success(
        self, auth_service: AuthService,
    ):
        user_id = str(1)

        access_token = auth_service.generate_access_token(
            user_id=user_id
        )
        decoded_user_id = auth_service.get_user_id_from_access_token(
            access_token=access_token
        )

        assert decoded_user_id == user_id

    async def test_google_auth_success(
        self, auth_service: AuthService,
    ):
        fake_code = 'fake_code'

        user = await auth_service.google_auth(code=fake_code)

        decoded_user_id = auth_service.get_user_id_from_access_token(
            access_token=user.access_token
        )

        assert user.user_id == decoded_user_id
        assert isinstance(user, UserLoginSchema)

    async def test_yandex_auth_success(self, auth_service: AuthService):
        fake_code = 'fake_code'

        user = await auth_service.yandex_auth(code=fake_code)
        decoded_user_id = auth_service.get_user_id_from_access_token(
            access_token=user.access_token
        )

        assert user.user_id == decoded_user_id
        assert isinstance(user, UserLoginSchema)


    async def test_login_success(
        self, auth_service: AuthService, user_profile: UserProfileFactory
    ):
        fake_username = user_profile.username
        fake_password = get_fake_password()

        user_profile=fake_password

        user = await auth_service.login(
            username=fake_username, password=fake_password
        )

        assert isinstance(user, UserLoginSchema)

    async def test_validate_auth_user_success(
        self, auth_service: AuthService, user_profile: UserProfileFactory
    ):
        fake_password = user_profile.password
        auth_service._validate_auth_user(user=user_profile, password=fake_password)

    async def test_validate_auth_user_without_user(
        self, auth_service: AuthService
    ):
        user_profile = None
        fake_password = get_fake_password()
        with pytest.raises(UserNotFoundException) as excinfo:
            auth_service._validate_auth_user(
                user=user_profile, password=fake_password
            )

        assert isinstance(excinfo.value, UserNotFoundException)
        assert excinfo.value.detail == UserNotFoundException.detail

    async def test_validate_auth_user_with_not_correct_password(
        self, auth_service: AuthService, user_profile: UserProfileFactory
    ):
        not_correct_password = 'not_correct_password'

        with pytest.raises(UserNotCorrectPasswordException) as excinfo:
            auth_service._validate_auth_user(
                user=user_profile, password=not_correct_password
            )

        assert isinstance(excinfo.value, UserNotCorrectPasswordException)
        assert excinfo.value.detail == UserNotCorrectPasswordException.detail
