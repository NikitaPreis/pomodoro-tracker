import pytest

from app.settings import Settings
from app.users.user_profile.service import UserService


@pytest.fixture
def user_service(auth_service, user_repository):
    return UserService(
        user_repository=user_repository,
        auth_service=auth_service
    )
