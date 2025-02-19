import pytest

from app.settings import Settings
from app.users.auth.service import AuthService


@pytest.fixture
def auth_service(google_client, yandex_client, user_repository):
    return AuthService(
        user_repository=user_repository,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client
    )
