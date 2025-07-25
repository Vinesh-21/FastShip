from fastapi import HTTPException
from typing import Annotated

from app.database.models import Seller
from app.utils import decode_access_token
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.services.shipment import ShipmentService

from app.services.seller import SellerService

#security
from app.core.security import oauth2_scheme

from uuid import UUID

# Asynchronous database session dep annotation
SessionDep = Annotated[AsyncSession, Depends(get_session)]


# Shipment service dep
def get_shipment_service(session: SessionDep):
    return ShipmentService(session)




# Shipment service dep annotation
ServiceDep = Annotated[
    ShipmentService,
    Depends(get_shipment_service),
]

def get_seller_service(session:SessionDep):
    return SellerService(session)

SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]




#Get Access Token From Header Of the Clent Request

async def get_access_token(token:str = Depends(oauth2_scheme))->dict:

    return await decode_access_token(token)

# Get Current Seller With Decoded Token Data

async def get_current_seller(data:Annotated[dict,Depends(get_access_token)],
                             session:SessionDep):
    return await session.get(Seller,UUID(data["user"]["id"]))
  

SellerDep = Annotated[Seller,Depends(get_current_seller)]