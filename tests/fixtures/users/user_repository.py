from dataclasses import dataclass

import pytest

from app.users.user_profile.schema import UserCreateSchema
from tests.fixtures.users.user_model import UserProfileFactory, get_fake_password, get_fake_user_id


@dataclass
class FakeUserRepository:
    async def get_user_by_email(self, email: str):
        return None

    async def create_user(self, user: UserCreateSchema):
        return UserProfileFactory(
            id=get_fake_user_id(),
            username=user.username,
            password=user.password,
            name=user.name,
            email=user.email,
            google_access_token=user.google_access_token,
            yandex_access_token=user.yandex_access_token
        )

    async def get_user_by_username(self, username: str):
        fake_password = get_fake_password()
        return UserProfileFactory(username=username,
                                  password=fake_password)


@pytest.fixture
def user_repository():
    return FakeUserRepository()
