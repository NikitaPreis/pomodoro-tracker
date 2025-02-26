from dataclasses import dataclass
import json

from aiokafka import AIOKafkaConsumer

from app.infrastructure.broker.accessor import get_broker_connection


@dataclass
class BrokerConsumer:
    consumer: AIOKafkaConsumer

    async def open_conntection(self) -> None:
        await self.consumer.start()

    async def close_connection(self) -> None:
        await self.consumer.stop()

    async def consume_callback_message(self) -> None:
        await self.open_conntection()

        try:
            async for message in self.consumer:
                print(message.value)
        finally:
            await self.close_connection()
