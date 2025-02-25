from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from app.consumer import make_amqp_consumer
from app.tasks.handlers import router as tasks_router
from app.users.auth.handlers import router as auth_router
from app.users.user_profile.handlers import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await make_amqp_consumer()
    yield


app = FastAPI(lifespan=lifespan)


router = APIRouter(
    prefix='/ping',
    tags=['ping']
)


@router.get('/db')
async def ping_db():
    from app.settings import settings
    print(settings.db_url)
    return {'message': 'ok'}


@router.get('/app')
async def ping_app():
    return {'text': 'app is working'}

app.include_router(router)
app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(user_router)
