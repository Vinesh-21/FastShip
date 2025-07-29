from fastapi import APIRouter


from app.api.routers.seller import router as seller_router
from app.api.routers.shipment import router as shipment_router
from app.api.routers.delivery_partner import router as deliveryPartner_router
master_router = APIRouter()

master_router.include_router(seller_router)
master_router.include_router(shipment_router)
master_router.include_router(deliveryPartner_router)


