from datetime import timedelta
from uuid import UUID
from fastapi import BackgroundTasks, HTTPException, status
from passlib.context import CryptContext
from app.services.notification import NotificationService
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.utils import decode_url_safe_token, generate_access_token, generate_url_safe_token


from .base import BaseService

from app.config import app_settings

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


class UserService(BaseService):
    def __init__(self, model: User, session: AsyncSession,tasks:BackgroundTasks):
        self.model = model
        self.session = session
        self.notification_service=NotificationService(tasks)

    async def _add_user(self, data: dict) -> User:
        user = self.model(
            **data,
            password_hash=password_context.hash(data["password"]),
        )
        return await self._add(user)

 

    async def _get_by_email(self, email) -> User | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )

    async def _generate_token(self, email, password) -> str:
        # Validate the credentials
        user = await self._get_by_email(email)

        if user is None or not password_context.verify(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or password is incorrect",
            )

        return generate_access_token(
            data={
                "user": {
                    "name": user.name,
                    "id": str(user.id),
                },
            }
        )

    async def send_password_reset_link(self, email, router_prefix):
        user = await self._get_by_email(email)

        token = generate_url_safe_token({"id": str(user.id)}, salt="password-reset")

        await self.notification_service.send_mail_with_template(
            recipients=[user.email],
            subject="FastShip Account Password Reset",
            context={
                "username": user.name,
                "reset_url": f"http://{app_settings.APP_DOMAIN}{router_prefix}/reset_password_form?token={token}",
            },
            template_name="mail_password_reset.html",
        )

    async def reset_password(self, token: str, password: str) -> bool:
        token_data = decode_url_safe_token(
            token,
            salt="password-reset",
            expiry=timedelta(days=1),
        )

        if not token_data:
            return False

        user = await self._get(UUID(token_data["id"]))
        user.password_hash = password_context.hash(password)

        await self._update(user)

        return True
