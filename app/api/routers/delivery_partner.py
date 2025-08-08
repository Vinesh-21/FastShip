from typing import Annotated

from app.core.security import TokenData
from app.database.models import DeliveryPartner
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import app_settings

from pydantic import EmailStr
from app.utils import TEMPLATE_DIR, invalidate_token
from fastapi.templating import Jinja2Templates

from ..dependencies import (
    DeliveryPartnerDep,
    DeliveryPartnerServiceDep,
    get_partner_access_token,
)
from ..schemas.delivery_partner import (
    DeliveryPartnerCreate,
    DeliveryPartnerRead,
    DeliveryPartnerResponse,
    DeliveryPartnerUpdate,
)

router = APIRouter(prefix="/partner", tags=["Delivery Partner"])
templates = Jinja2Templates(TEMPLATE_DIR)


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

@router.get("/partner/me", response_model=DeliveryPartnerResponse, name="getDeliveryPartnerProfile")
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


### Forget Password (send reset link)
@router.get("/forgot_password", name="forgotPasswordPartner")
async def forget_password_partner(email: EmailStr, service: DeliveryPartnerServiceDep):

    await service.send_password_reset_link(email, router.prefix)
    return {"detail": "Check email for password reset link"}


### Reset Password Form (hidden from OpenAPI)
@router.get("/reset_password_form", include_in_schema=False)
async def get_reset_password_form(request: Request, token: str):

    return templates.TemplateResponse(
        request=request,
        name="password/reset.html",
        context={
            "reset_url": f"http://{app_settings.APP_DOMAIN}{router.prefix}/reset_password?token={token}"
        },
    )


### Reset Password (form submit)
@router.post("/reset_password", include_in_schema=False)
async def reset_password_partner(
    request: Request,
    token: str,
    password: Annotated[str, Form()],
    service: DeliveryPartnerServiceDep,
):

    is_success = await service.reset_password(token, password)

    return templates.TemplateResponse(
        request=request,
        name="password/reset_success.html" if is_success else "password/reset_failed.html",
    )