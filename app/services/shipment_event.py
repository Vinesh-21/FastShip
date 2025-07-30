

from app.services.base import BaseService
from app.database.models import Shipment, ShipmentEvent, ShipmentStatus
from app.services.notification import NotificationService


class ShipmentEventService(BaseService):
    
    def __init__(self,session,tasks):

        super().__init__(ShipmentEvent,session)
        self.notification_service = NotificationService(tasks)

    async def add(self,
                  shipment:Shipment,
                  location:int = None ,
                  status:ShipmentStatus = None,
                  description:str|None =None) -> ShipmentEvent:
        
        if not location:
            last_event = await self.get_latest_event(shipment)
            location = last_event.location
        if not status:
            last_event = await self.get_latest_event(shipment)
            status = last_event.status

        new_event = ShipmentEvent(location=location,
                                  status=status,
                                  description=description if description else self._generate_description(status,location),
                                  shipment_id=shipment.id)
        

        await self._notif(shipment,status)

        return await self._add(new_event)
    
    async def get_latest_event(self,shipment:Shipment):
        timeline = shipment.timeline

        timeline.sort(key= lambda event: event.created_at)

        return timeline[-1]
    

    def _generate_description(self, status: ShipmentStatus, location: int):
        match status:
            case ShipmentStatus.placed:
                return "assigned delivery partner"
            case ShipmentStatus.out_for_delivery:
                return "shipment out for delivery"
            case ShipmentStatus.delivered:
                return "successfully delivered"
            case ShipmentStatus.cancelled:
                return "Cancelled by the seller"
            case _: 
                return f"scanned at {location}"

    async def _notif(self, shipment: Shipment, status: ShipmentStatus):

        if status == ShipmentStatus.in_transit:
            return

        match status:
            case ShipmentStatus.placed:

                await self.notification_service.send_mail_with_template(
                    recipients=[shipment.client_contact_email],
                    subject="Your Order is Placed 📦",
                    context={"subject":"Your Order is Placed 📦",
                             "seller":shipment.seller.name,
                             "delivery_partner":shipment.delivery_partner.name,
                             "status":"Placed",
                             "description":"Thank you for your order!"
                             },
                    template_name="mail_placed.html"
                    )


            case ShipmentStatus.out_for_delivery:
                await self.notification_service.send_mail_with_template(
                    recipients=[shipment.client_contact_email],
                    subject="Your Order is Out for Delivery! 🚚",
                   context = {
                        "subject": "Your Order is Out for Delivery! 🚚",
                        "seller": shipment.seller.name,
                        "delivery_partner": shipment.delivery_partner.name,
                        "status": "Out for Delivery",
                        "description": "Please ensure someone is available to receive it."
                        },
                    template_name="mail_out_for_delivery.html"
                    )


            case ShipmentStatus.cancelled:
                await self.notification_service.send_mail_with_template(
                    recipients=[shipment.client_contact_email],
                    subject="Your Order Has Been Cancelled ❌",
                    context={
                        "subject": "Your Order Has Been Cancelled ❌",
                        "seller": shipment.seller.name,
                        "delivery_partner": shipment.delivery_partner.name,
                        "status": "Cancelled",
                        "description": "If you have already paid, a refund will be processed shortly."
                    },
                    template_name="mail_cancelled.html"
                )
            case ShipmentStatus.delivered:
                await self.notification_service.send_mail_with_template(
                        recipients=[shipment.client_contact_email],
                        subject="Your Order Has Been Delivered! 🎉",
                        context={
                            "subject": "Your Order Has Been Delivered! 🎉",
                            "seller": shipment.seller.name,
                            "delivery_partner": shipment.delivery_partner.name,
                            "status": "Delivered",
                            "description": "We hope you enjoy your purchase! Thank you for shopping with us."
                        },
                        template_name="mail_delivered.html"
                    )