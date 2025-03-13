from dataclasses import dataclass

from app.users.auth.schema import UserLoginSchema
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.schema import UserCreateSchema
from app.users.user_settings.service import UserSettingsService


@dataclass
class UserService:
    user_repository: UserRepository
    user_settings_service: UserSettingsService
    auth_service: AuthService

    async def create_user(self, user: UserCreateSchema) -> UserLoginSchema:
        user = await self.user_repository.create_user(user=user)
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        await self.user_settings_service.create_user_settings(
            user_id=user.id
        )
        return UserLoginSchema(
            user_id=user.id, access_token=access_token
        )
