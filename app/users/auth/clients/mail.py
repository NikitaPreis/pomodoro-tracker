from dataclasses import dataclass
import json
from uuid import uuid4

import aio_pika

from app.broker.producer import BrokerProducer
from app.settings import Settings


@dataclass
class MailClient:
    settings: Settings
    broker_producer: BrokerProducer

    async def send_welcom_email(self, to: str) -> None:
        email_body = {
            'message': 'Welcome to pomodoro',
            'user_email': to,
            'subject': 'Welcom message',
            'correlation_id': str(uuid4)
        }

        await self.broker_producer.send_welcome_email(email_data=email_body)
        return
