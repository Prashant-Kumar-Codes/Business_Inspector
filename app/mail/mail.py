from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from app.config.config import settings

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_DEFAULT_SENDER,
    MAIL_PORT=settings.MAIL_PORT or 587,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_USE_TLS,  # True for TLS (port 587)
    MAIL_SSL_TLS=False,                   # True only if using SSL direct (port 465)
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

mail = FastMail(mail_config)