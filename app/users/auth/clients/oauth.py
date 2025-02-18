from dataclasses import dataclass

import httpx

from app.settings import Settings


@dataclass
class OAuthClient:
    """
    Базовый класс для клиента аутентификации с OAuth.
    """

    settings: Settings

    def get_user_info(self, code: str):
        pass

    def _get_user_access_token(self, code: str) -> str:
        pass
