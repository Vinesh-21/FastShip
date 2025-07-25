from app.utils import decode_access_token, invalidate_token
from fastapi import APIRouter,Depends

from app.database.models import Seller

from typing import Annotated

#SCHEMA-REQUEST-VALIDATION
from app.api.schemas.seller import SellerCreate,SellerRead


#Oauth2
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import oauth2_scheme


from app.api.dependencies import SellerServiceDep, SessionDep, get_access_token

router = APIRouter(prefix="/seller",tags=["Seller"])


@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service:SellerServiceDep ):
    
    response = await service.add(seller)

    return response


@router.post("/login" )
async def login_seller(request_form:Annotated[OAuth2PasswordRequestForm,Depends()],service:SellerServiceDep):

    jwt_token = await service.authenticate(email=request_form.username,password=request_form.password)
    return {"access_token": jwt_token, "type": "jwt"}



@router.get("/logout" )
async def logout_seller(token_data:Annotated[dict,Depends(get_access_token)]):
    print(token_data)
    print(type(token_data))
    print(token_data["user"])
    print(token_data["exp"])
    print(token_data["jti"])
    
    await invalidate_token(token_data)












# ----------------------------
# PROTECTED ROUTE EXPLANATION
# ----------------------------
# this is a protected route – only accessible by logged-in users
# to make this route protected, the client (browser or frontend app like React) 
# needs to send the access token (JWT) in the Authorization header of the request
#
# STEP 1: user logs in using their email and password → `/login` endpoint
# STEP 2: server verifies credentials and generates a JWT access token if valid
# STEP 3: the client stores this token (usually in localStorage or memory)
# STEP 4: for any protected routes like `/dashboard`, client sends a request with:
#         Authorization: Bearer <access_token>
# STEP 5: FastAPI uses a dependency to extract and decode the token
# STEP 6: it verifies the signature using the secret key and algorithm (e.g., HS256)
# STEP 7: if token is valid and not expired → we allow access and pass the user info
# STEP 8: if token is invalid or expired → FastAPI automatically raises 401 Unauthorized
#
# this whole flow ensures that only authenticated users can access this route


