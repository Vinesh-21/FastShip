from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.seller import SellerCreate
from app.database.models import Seller


from app.services.user import UserService

### Business Logic For Seller  
class SellerService(UserService):
    def __init__(self, session: AsyncSession,tasks:BackgroundTasks):
        super().__init__(Seller, session,tasks)

    # Add Seller
    async def add(self, seller_create: SellerCreate) -> Seller:
        return await self._add_user(
            seller_create.model_dump()
        )

    # Generate JWT Token For Login
    async def token(self, email, password) -> str:
        return await self._generate_token(email, password)
