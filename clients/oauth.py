from dataclasses import dataclass

import requests

from settings import Settings
from schema import GoogleUserData


@dataclass
class OAuthClient:
    """
    Базовый класс для клиента аутентификации с OAuth.
    """

    settings: Settings

    def get_user_info(self, code: str) -> GoogleUserData:
        pass

    def _get_user_access_token(self, code: str) -> str:
        pass
