from uuid import UUID
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse

from ..dependencies import DeliveryPartnerDep, SellerDep, ShipmentServiceDep
from ..schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate

# JINJA
from fastapi.templating import Jinja2Templates

from app.utils import TEMPLATE_DIR


router = APIRouter(prefix="/shipment", tags=["Shipment"])

# Templeting Engine
templates = Jinja2Templates(TEMPLATE_DIR)



### Read a shipment by id
@router.get("/", response_model=ShipmentRead,name="getShipment")
async def get_shipment(id: UUID, service: ShipmentServiceDep):
    # Check for shipment with given id
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment


# Tracking shipment
@router.get("/track",include_in_schema=False)
async def get_tracking(request:Request,id: UUID, service: ShipmentServiceDep):
    
    shipment = await service.get(id)

    context = shipment.model_dump()
    context["status"] = shipment.status
    context["partner"] = shipment.delivery_partner.name
    context["timeline"] = shipment.timeline
    context["timeline"].reverse()

    return templates.TemplateResponse(
        request=request,
        name="track.html",
        context=context,
    )

### Create a new shipment
@router.post("/", response_model=ShipmentRead ,
             name="createShipment",
             description="Create A New Shipment",
             status_code=status.HTTP_201_CREATED,
             responses={
                 status.HTTP_201_CREATED: {"description": "Shipment successfully created."},
                 status.HTTP_406_NOT_ACCEPTABLE: {"description": "No delivery partner available at the moment."},
             })
async def submit_shipment(
    seller: SellerDep,
    shipment: ShipmentCreate,
    service: ShipmentServiceDep,
):
    return await service.add(shipment, seller)


### Update fields of a shipment
@router.patch("/", response_model=ShipmentRead,name="updateShipment")
async def update_shipment(
    id: UUID,
    shipment_update: ShipmentUpdate,
    partner: DeliveryPartnerDep,
    service: ShipmentServiceDep,
):
    # Update data with given fields
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )
    

    return await service.update(id,shipment_update,partner)


### cancel a shipment by id
@router.get("/cancel",response_model=ShipmentRead,name="cancelShipment")
async def delete_shipment(id: UUID, seller:SellerDep,service: ShipmentServiceDep) -> dict[str, str]:
    # Remove from database
    return await service.cancel(id,seller)


