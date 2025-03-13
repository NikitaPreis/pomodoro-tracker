from contextlib import asynccontextmanager
from time import sleep

from aiormq.exceptions import AMQPConnectionError
from fastapi import FastAPI

from app.consumer import make_amqp_consumer
from app.infrastructure.database.accessor import init_models


async def ampq_con(attempts_to_connection: int = 3):
    """Retry connecting to RabbitMQ.
    
    This is now necessary because application backend
    container starts before RabbitMQ container.

    The "depends on" option from docker-compose file can't fix this problem.
    So we use this solution until we find a better one.
    """
    try:
        await make_amqp_consumer()
    except AMQPConnectionError as e:
        print(f'AMQP Connection Error: {e.reason}.')
        attempts_to_connection -= 1
        sleep(5)
        print(f'Only {attempts_to_connection} attempts left'
              f'to create AMQP Connection.')
        if attempts_to_connection <= 0:
            await ampq_con(attempts_to_connection=attempts_to_connection)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Init SQLAlchemy models and create a connection to RabbitMQ."""
    await init_models()
    await ampq_con()
    yield
