from fastapi import BackgroundTasks
from fastapi_mail import FastMail,ConnectionConfig,MessageSchema,MessageType

from app.config import notification_settings,twilio_settings
from pydantic import EmailStr
from app.utils import TEMPLATE_DIR

from twilio.rest import Client

### Notification Service
class NotificationService:
    def __init__(self,tasks:BackgroundTasks):

        ### FastMail(SMTP) For Mailing
        self.fastmail = FastMail(
            ConnectionConfig(
                **notification_settings.model_dump(),
                TEMPLATE_FOLDER=TEMPLATE_DIR,
            )
        )

        self.tasks =tasks
        
        ### Twilio Client For SMS
        self.twilio_client =Client(
            twilio_settings.TWILIO_SID,
            twilio_settings.TWILIO_AUTH_TOKEN
        )



    ### Send Mail
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

    ### Send Mail
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
    ### Send SMS
    async def send_sms(self,to:str, body:str):
        self.tasks.add_task(
            self.twilio_client.messages.create,
            from_=twilio_settings.TWILIO_NUMBER,
            to=to,
            body=body
)