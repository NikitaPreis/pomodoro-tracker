import pytest

from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.service import UserService
from app.users.user_profile.schema import UserCreateSchema
from tests.fixtures.users.user_model import UserProfileFactory, get_fake_user_id


class TestUserService:

    async def test_create_user_success(
        self, user_service: UserService, user_profile: UserProfileFactory,
    ):
        fake_user_id = get_fake_user_id()
        user_profile.id = fake_user_id
        user: UserLoginSchema = await user_service.create_user(user=user_profile)

        assert isinstance(user, UserLoginSchema)
        assert user.user_id == user_profile.id
