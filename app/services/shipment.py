from uuid import UUID
from fastapi import HTTPException

from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.shipment import ShipmentCreate
from app.database.models import Shipment, ShipmentStatus

from uuid import UUID

class ShipmentService:
    def __init__(self, session: AsyncSession):
        # Get database session to perform database operations
        self.session = session

    # Get a shipment by id 
    async def get(self, id: UUID) -> Shipment:
        result= await self.session.get(Shipment, id)
        return result

    # Add a new shipment
    async def add(self, shipment_create: ShipmentCreate,id:UUID) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id=id
        )
        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)

        return new_shipment

    # Update an existing shipment
    async def update(self, id: UUID, shipment_update: dict) -> Shipment:
        shipment = await self.get(id)
        shipment.sqlmodel_update(shipment_update)

        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)

        return shipment

    # Delete a shipment
    async def delete(self, id: UUID) -> None:
        await self.session.delete(await self.get(id))
        await self.session.commit()