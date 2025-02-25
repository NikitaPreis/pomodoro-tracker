from dataclasses import dataclass
import json
from uuid import uuid4

import aio_pika

from app.settings import Settings


@dataclass
class MailClient:
    settings: Settings

    async def send_welcom_email(self, to: str) -> None:
        connection = await aio_pika.connect_robust(self.settings.AMQP_URL)
        email_body = {
            'message': 'Welcome to pomodoro',
            'user_email': to,
            'subject': 'Welcom message'
        }

        async with connection:
            channel = await connection.channel()
            message = aio_pika.Message(
                body=json.dumps(email_body).encode(),
                correlation_id=str(uuid4()),
                reply_to='callback_mail_queue'
            )
            await channel.default_exchange.publish(
                message=message,
                routing_key='mail_queue'
            )
        return
