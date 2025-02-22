import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.settings import Settings
from worker.celery import send_email_task

class MailClient:

    @staticmethod
    def send_welcom_email(to: str) -> None:
        return send_email_task.delay(
            subject='Welcome email',
            text=f'Welcome to pomodoro, {to}!',
            to=to
        )
