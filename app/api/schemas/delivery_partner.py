from pydantic import BaseModel,EmailStr


class BaseDeliveryPartner(BaseModel):
    name: str
    email: EmailStr
    Servicable_zip_code :list[int]
    max_handling_capacity:int
 
class DeliveryPartnerRead(BaseDeliveryPartner):
    pass

class DeliveryPartnerUpdate(BaseModel):
    Servicable_zip_code :list[int]
    max_handling_capacity:int


class DeliveryPartnerCreate(BaseDeliveryPartner):
    password: str