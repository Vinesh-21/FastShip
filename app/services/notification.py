from dns import message
from fastapi_mail import FastMail,ConnectionConfig,MessageSchema,MessageType

from app.config import notification_settings
from pydantic import EmailStr
from app.utils import TEMPLATE_DIR


class NotificationService:
    def __init__(self,tasks):
        self.fastmail = FastMail(
            ConnectionConfig(
                **notification_settings.model_dump(),
                TEMPLATE_FOLDER=TEMPLATE_DIR,
            )
        )

        self.tasks =tasks




    async def send_email(self,recipients: list[EmailStr],subject: str,body: str):

        self.tasks.add_task(
            self.fastmail.send_message,
             message=MessageSchema(
                recipients=recipients,
                subject=subject,
                body=body,
                subtype=MessageType.plain
            )   
        )

    async def send_mail_with_template(self,recipients: list[EmailStr],subject: str,context: dict,template_name:str):
        self.tasks.add_task(
            self.fastmail.send_message,
            message=MessageSchema(
                recipients=recipients,
                subject=subject,
                template_body=context,
                subtype=MessageType.html
            ),
            template_name=template_name
        )