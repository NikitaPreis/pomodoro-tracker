import pytest

from app.users.user_profile.service import UserService


@pytest.fixture
def user_service(mock_auth_service, fake_user_repository):
    return UserService(
        user_repository=fake_user_repository,
        auth_service=mock_auth_service
    )
