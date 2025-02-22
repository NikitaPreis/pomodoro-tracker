import pytest

from app.settings import Settings
from app.users.auth.clients import MailClient
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository


@pytest.fixture
def mock_auth_service(google_client, yandex_client, fake_user_repository):
    return AuthService(
        user_repository=fake_user_repository,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
        mail_client=MailClient()
    )


@pytest.fixture
def auth_service(
    google_client, yandex_client, get_db_session
) -> AuthService:
    return AuthService(
        user_repository=UserRepository(
            db_session=get_db_session
        ),
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
        mail_client=MailClient()
    )
