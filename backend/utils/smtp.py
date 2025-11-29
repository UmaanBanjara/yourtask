from fastapi_mail import FastMail , ConnectionConfig , MessageSchema
import os
from dotenv import load_dotenv
from typing import List
from pydantic import EmailStr


load_dotenv()

#connection config
conf = ConnectionConfig(
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False

)

#mail function
async def send_mail(subject : str , to : List[EmailStr] , body : str):
    message = MessageSchema(
        subject=subject,
        body = body,
        subtype="html",
        recipients=to
    )
    fm = FastMail(conf)
    await fm.send_message(message)