import asyncio
from typing import Annotated
import json

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from fastapi import Depends, Request, security, Security, HTTPException
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.broker import BrokerProducer
from app.broker.consumer import BrokerConsumer
from app.infrastructure.cache import get_redis_connection
from app.users.auth.clients import GoogleClient, YandexClient, MailClient
from app.infrastructure.database import get_db_session
from app.exception import TokenExpired, TokenNotCorrect
from app.tasks.repository import TaskRepository, TaskCache
from app.users.user_profile.repository import UserRepository
from app.tasks.service import TaskService
from app.users.auth.service import AuthService
from app.users.user_profile.service import UserService
from app.settings import Settings


# ~~~~~~~~~~~~~~~ Broker Dependencies ~~~~~~~~~~~~~~~


event_loop = asyncio.get_event_loop()


async def get_broker_producer() -> BrokerProducer:
    settings = Settings()
    return BrokerProducer(
        producer=AIOKafkaProducer(
            bootstrap_servers=settings.BROKER_URL,
            loop=event_loop,
        ),
        email_topic=settings.EMAIL_TOPIC
    )


async def get_broker_consumer() -> BrokerConsumer:
    settings = Settings()
    return BrokerConsumer(
        consumer=AIOKafkaConsumer(
            settings.EMAIL_CALLBACK_TOPIC,
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda message: json.loads(
                message.decode('utf-8')
                )
        ),
    )


# ~~~~~~~~~~~~~~~ Client Dependencies ~~~~~~~~~~~~~~~


async def get_mail_client(
    broker_producer: BrokerProducer = Depends(get_broker_producer),
) -> MailClient:
    return MailClient(
        settings=Settings(),
        broker_producer=broker_producer,
    )


async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()


async def get_google_client(
    async_client: httpx.AsyncClient = Depends(get_async_client)
) -> GoogleClient:
    return GoogleClient(settings=Settings(), async_client=async_client)


async def get_yandex_client(
    async_client: httpx.AsyncClient = Depends(get_async_client)
) -> YandexClient:
    return YandexClient(settings=Settings(), async_client=async_client)


# ~~~~~~~~~~~~~~~ Repository Dependencies ~~~~~~~~~~~~~~~


async def get_tasks_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> TaskRepository:
    return TaskRepository(db_session)


async def get_user_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_cache_tasks_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)


# ~~~~~~~~~~~~~~~ Service Dependencies ~~~~~~~~~~~~~~~


async def get_task_service(
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
    task_cache: Annotated[TaskCache, Depends(get_cache_tasks_repository)]
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache
    )


async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    google_client: GoogleClient = Depends(get_google_client),
    yandex_client: YandexClient = Depends(get_yandex_client),
    mail_client: MailClient = Depends(get_mail_client)
) -> AuthService:
    return AuthService(
        user_repository=user_repository, settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
        mail_client=mail_client
    )


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(
        user_repository=user_repository, auth_service=auth_service
    )


# ~~~~~~~~~~~~~~~ Handlers Dependencies ~~~~~~~~~~~~~~~


resuable_oauth2 = security.HTTPBearer()


async def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: security.http.HTTPAuthorizationCredentials = Security(resuable_oauth2)
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(
            token.credentials
        )
    except TokenExpired as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    except TokenNotCorrect as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    return user_id
