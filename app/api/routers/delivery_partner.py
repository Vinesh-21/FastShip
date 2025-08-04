from typing import Annotated

from app.core.security import TokenData
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.utils import invalidate_token

from ..dependencies import (
    DeliveryPartnerDep,
    DeliveryPartnerServiceDep,
    get_partner_access_token,
)
from ..schemas.delivery_partner import (
    DeliveryPartnerCreate,
    DeliveryPartnerRead,
    DeliveryPartnerUpdate,
)

router = APIRouter(prefix="/partner", tags=["Delivery Partner"])


### Register a new delivery partner
@router.post("/signup", response_model=DeliveryPartnerRead,name="signupDeliveryPartner")
async def register_delivery_partner(
    seller: DeliveryPartnerCreate,
    service: DeliveryPartnerServiceDep,
):
    return await service.add(seller)


### Login a delivery partner
@router.post("/token",response_model=TokenData,name="loginDeliveryPartner")
async def login_delivery_partner(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: DeliveryPartnerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt",
    }

@router.get("/me", response_model=DeliveryPartnerRead, name="getDeliveryPartnerProfile")
async def get_partner_profile(
    partner: DeliveryPartnerDep,
) -> DeliveryPartnerDep:
    return partner


### Update the logged in delivery partner
@router.post("/", response_model=DeliveryPartnerRead,name="updateDeliveryPartner")
async def update_delivery_partner(
    partner_update: DeliveryPartnerUpdate,
    partner: DeliveryPartnerDep,
    service: DeliveryPartnerServiceDep,
):
    # Update data with given fields
    update = partner_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    return await service.update(
        partner.sqlmodel_update(update),
    )


### Logout a delivery partner
@router.get("/logout",name="logoutDeliveryPartner")
async def logout_delivery_partner(
    token_data: Annotated[dict, Depends(get_partner_access_token)],
):
    await invalidate_token(token_data)
    return {"detail": "Successfully logged out"}
