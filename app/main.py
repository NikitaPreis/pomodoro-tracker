from contextlib import asynccontextmanager
from typing import Annotated
from time import sleep

from aiormq.exceptions import AMQPConnectionError
from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.categories.handlers import router as category_router
from app.consumer import make_amqp_consumer
from app.infrastructure.database.accessor import get_db_session, init_models
from app.core.tasks.handlers import router as tasks_router
from app.users.auth.handlers import router as auth_router
from app.users.user_profile.handlers import router as user_router


async def ampq_con(attempts_to_connection: int = 3):
    try:
        await make_amqp_consumer()
    except AMQPConnectionError as e:
        print(f'AMQP Connection Error: {e.reason}.')
        attempts_to_connection =- 1
        sleep(5)
        print(f'{attempts_to_connection} attempts left to create AMQP Connection')
        if attempts_to_connection <= 0:
            await ampq_con(attempts_to_connection=attempts_to_connection)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    await ampq_con()
    yield


app = FastAPI(lifespan=lifespan)


router = APIRouter(
    prefix='/ping',
    tags=['ping']
)


@router.get('/app')
async def ping_app():
    return {'text': 'app is working'}


@router.get('/db')
async def ping_db(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
):
    async with db_session as session:
        try:
            await session.execute(text('SELECT 1'))
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail='Database is not available'
            )
    return {'message': 'database is working'}

app.include_router(router)
app.include_router(tasks_router)
app.include_router(category_router)
app.include_router(auth_router)
app.include_router(user_router)
