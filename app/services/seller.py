#FASTAPI
from app.utils import genereate_access_token
from fastapi import HTTPException, status

#Datetime
from datetime import datetime, timedelta

#SQLMODEL SCHEMA
from app.api.schemas.seller import SellerCreate

#DB
#Async SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession
#Query
from sqlalchemy import select
#MODELS
from app.database.models import Seller

#Password Hashing
from passlib.context import CryptContext
import jwt 

#Config
from app.config import security_settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class SellerService:
    def __init__(self,session:AsyncSession):
        self.session = session

    async def add(self,credentials: SellerCreate):

        
        new_seller = Seller(
            **credentials.model_dump(exclude=["password"]),
            password_hash=password_context.hash(credentials.password),
            )
        
        self.session.add(new_seller)
        await self.session.commit()
        await self.session.refresh(new_seller)
        return new_seller
    

    async def authenticate(self, email: str, password: str) -> str:
        #validate the email and password

        result = await self.session.execute(
            select(Seller).where(Seller.email == email)
         )
        

        seller=result.scalar()


        if seller is None or not (password_context.verify(password, seller.password_hash)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or password is incorrect"
            )
            
        jwt_token = genereate_access_token(
            data={
            "user":{
                "name":seller.name,
                "id":str(seller.id)
            },

        }
        )



        return jwt_token
    