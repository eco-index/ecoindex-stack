from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM, MAIL_PORT, MAIL_SERVER, MAIL_FROM_NAME
from app.models.email import EmailSchema

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER='/backend/templates/email'
)

class EmailService:
    async def send_email_async(self, email: EmailSchema):
        message = MessageSchema(
            subject=email.subject,
            recipients=email.dict().get("email"),
            template_body=email.dict().get("body"),
        )
        
        fm = FastMail(conf)
        await fm.send_message(message, template_name='email.html')
        return True

    def send_email_background(self, background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict):
        message = MessageSchema(
            subject=subject,
            recipients=[email_to],
            body=body,
            subtype='html',
        )
        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, message, template_name='email.html')
