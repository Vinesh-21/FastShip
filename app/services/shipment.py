from datetime import datetime, timedelta
from uuid import UUID

from app.services.shipment_event import ShipmentEventService
from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate
from app.database.models import DeliveryPartner, Seller, Shipment, ShipmentStatus

from app.services.base import BaseService
from app.services.delivery_partner import DeliveryPartnerService


class ShipmentService(BaseService):
    def __init__(
        self,
        session: AsyncSession,
        partner_service: DeliveryPartnerService,
        event_service: ShipmentEventService
    ):
        super().__init__(Shipment, session)
        self.partner_service = partner_service
        self.event_service = event_service

    # Get a shipment by id
    async def get(self, id: UUID) -> Shipment | None:
        return await self._get(id)

    # Add a new shipment
    async def add(self, shipment_create: ShipmentCreate, seller: Seller) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id=seller.id,
        )
        # Assign delivery partner to the shipment
        partner = await self.partner_service.assign_shipment(
            new_shipment,
        )
        # Add the delivery partner foreign key
        new_shipment.delivery_partner_id = partner.id


        shipment_with_UUID = await self._add(new_shipment)#Beacause we cannot access the UUID IS GENERATED So we save and use the UUID
        event =await self.event_service.add(shipment=shipment_with_UUID,
                               location=seller.zip_code,
                               status=ShipmentStatus.placed,
                               description=f"assigned to a {partner.name}")
        shipment_with_UUID.timeline.append(event)
        return shipment_with_UUID

    # Update an existing shipment
    async def update(self, UUID: UUID,shipment_update:ShipmentUpdate,partner:DeliveryPartner) -> Shipment:
        # Validate logged in parter with assigned partner
        # on the shipment with given id
        shipment = await self.get(UUID)

        if shipment.delivery_partner_id != partner.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized",
            )
        
        update = shipment_update.model_dump(exclude_none=True)

        if shipment_update.estimated_delivery:
            shipment.estimated_delivery = shipment_update.estimated_delivery

        # Event is added only when there is a meaningful update, such as:
        # - More than just estimated_delivery is being updated
        # - OR, estimated_delivery is not provided (implying status or location is being updated)
        if (len(update) > 1)  or not shipment_update.estimated_delivery:
            await self.event_service.add(
                shipment=shipment,
                **update,
            )

        return await self._update(shipment)


    async def cancel(self,id:UUID,seller:Seller)->Shipment:
        shipment =await self.get(id)
        if shipment.seller.id != seller.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Not Authorized")
        event = await self.event_service.add(
            shipment=shipment,
            status=ShipmentStatus.cancelled
        )

        shipment.timeline.append(event)

        return shipment
    # Delete a shipment
    async def delete(self, id: int) -> None:
        await self._delete(await self.get(id))
