from dataclasses import dataclass
import datetime as dt
from datetime import timedelta

from jose import jwt, JWTError

from app.users.auth.clients import GoogleClient, YandexClient, MailClient
from app.exception import (UserNotFoundException,
                           UserNotCorrectPasswordException,
                           TokenExpired, TokenNotCorrect,
                           UserSettingsCreatingException)
from app.users.user_profile.models import UserProfile
from app.users.user_profile.repository import UserRepository
from app.users.user_settings.service import UserSettingsService
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.schema import UserCreateSchema
from app.settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    user_settings_service: UserSettingsService
    google_client: GoogleClient
    yandex_client: YandexClient
    mail_client: MailClient
    settings: Settings

    def get_google_redirect_url(self) -> str:
        print(self.settings.google_redirect_url)
        return self.settings.google_redirect_url

    async def google_auth(self, code: str):
        user_data = await self.google_client.get_user_info(code=code)

        if user := await self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)
        create_user_data = UserCreateSchema(
            google_access_token=user_data.access_token,
            email=user_data.email,
            name=user_data.name
        )
        created_user = await self.user_repository.create_user(
            create_user_data
        )
        access_token = self.generate_access_token(user_id=created_user.id)

        await self.user_settings_service.create_user_settings(
            user_id=created_user.id
        )
        await self.mail_client.send_welcom_email(to=user_data.email)
        return UserLoginSchema(
            user_id=created_user.id, access_token=access_token
        )

    def get_yandex_redirect_url(self) -> str:
        print(self.settings.yandex_redirect_url)
        return self.settings.yandex_redirect_url

    async def yandex_auth(self, code: str) -> UserLoginSchema:
        user_data = await self.yandex_client.get_user_info(code=code)

        if user := await self.user_repository.get_user_by_email(email=user_data.default_email):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)
        create_user_data = UserCreateSchema(
            yandex_access_token=user_data.access_token,
            email=user_data.default_email,
            name=user_data.name
        )
        created_user = await self.user_repository.create_user(
            create_user_data
        )
        access_token = self.generate_access_token(user_id=created_user.id)
        await self.user_settings_service.create_user_settings(
            user_id=created_user.id
        )
        await self.mail_client.send_welcom_email(to=user_data.default_email)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username=username)
        self._validate_auth_user(user=user, password=password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(
            user_id=user.id, access_token=access_token
        )

    def generate_access_token(self, user_id: int) -> str:

        payload = {
            'user_id': user_id,
            'expire': (dt.datetime.now(tz=dt.UTC) + timedelta(
                days=7
            )).timestamp()
        }

        encoded_jwt = jwt.encode(
            payload, self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ENCODE_ALHORITHM
        )
        return encoded_jwt


    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(
                access_token, self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ENCODE_ALHORITHM]
            )
        except JWTError:
            raise TokenNotCorrect
        if payload['expire'] < dt.datetime.now().timestamp():
            raise TokenExpired
        return payload['user_id']

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException
