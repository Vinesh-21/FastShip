from typing import Annotated

from app.core.security import TokenData
from fastapi import APIRouter, Depends, Form, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.utils  import TEMPLATE_DIR, invalidate_token
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from app.config import app_settings

from app.api.dependencies import SellerDep, SellerServiceDep, get_seller_access_token
from ..schemas.seller import SellerCreate, SellerRead

router = APIRouter(prefix="/seller", tags=["Seller"])


### Register a new seller
@router.post("/signup", response_model=SellerRead,name="signupSeller")
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    return await service.add(seller)


### Login a seller
@router.post("/token",response_model=TokenData,name="loginSeller")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt",
    }

@router.get("/seller/me", response_model=SellerRead,name="getSellerProfile")
async def get_seller_profile(seller: SellerDep)->SellerDep:
    return seller

### Logout a seller
@router.get("/logout",name="logoutSeller")
async def logout_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token)],
):
    await invalidate_token(token_data)
    return {
        "detail": "Successfully logged out"
    }


### Forget Password
@router.get("/forgot_password",name="forgotPassword")
async def forget_password(email:EmailStr,service: SellerServiceDep):
    await service.send_password_reset_link(email,router.prefix)
    return {"detail": "Check email for password reset link"}

# Templating Engine 
templates = Jinja2Templates(TEMPLATE_DIR)
### Reset Password Form
@router.get("/reset_password_form",include_in_schema=False)
async def get_reset_password_form(request: Request, token: str):

    return templates.TemplateResponse(
        request=request,
        name="password/reset.html",
        context={
            "reset_url": f"http://{app_settings.APP_DOMAIN}{router.prefix}/reset_password?token={token}"
        }
    )


### Reset Password 
@router.post("/reset_password")
async def reset_password(
    request: Request,
    token: str,
    password: Annotated[str, Form()],
    service: SellerServiceDep,
):
    is_success = await service.reset_password(token, password)

    return templates.TemplateResponse(
        request=request,
        name="password/reset_success.html" if is_success else "password/reset_failed.html",
    )
