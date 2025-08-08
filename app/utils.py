from datetime import datetime, timedelta, timezone
from pathlib import Path
import jwt

from fastapi import HTTPException, status

from app.config import security_settings

from uuid import UUID, uuid4

from app.database.mongodb import blacklist_collection,otp_collection

#itsDangerous
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

APP_DIR = Path(__file__).resolve().parent

TEMPLATE_DIR = APP_DIR/"templates"

_serializer = URLSafeTimedSerializer(security_settings.JWT_SECERET_KEY)



def generate_access_token(
    data: dict,
    expiry: timedelta = timedelta(days=7),
) -> str:
    return jwt.encode(
        payload={
            **data,
            "jti": str(uuid4()),
            "exp": datetime.now(timezone.utc) + expiry,
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECERET_KEY,
    )


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            jwt=token,
            key=security_settings.JWT_SECERET_KEY,
            algorithms=[security_settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError:
        return None


async def is_jti_blacklisted(jti:str):
    record = await blacklist_collection.find_one({"jti":jti})
    return record is not None


async def invalidate_token(payload:dict):


    jti=str(payload["jti"])
    exp=datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    await blacklist_collection.insert_one({"jti":jti,"exp":exp})
    print("invalitadated user",payload["user"])



def generate_url_safe_token(data:dict,salt:str|None =None)->str:
    return _serializer.dumps(data,salt=salt)


def decode_url_safe_token(token:str,salt:str|None =None,expiry: timedelta | None = None):
    try:
        return _serializer.loads(
            token,
            salt=salt,
            max_age=expiry.total_seconds() if expiry else None,
        )
    except (BadSignature, SignatureExpired):
        return None
    
async def add_shipment_verfication_otp(id:UUID ,otp:int,expiry:timedelta = timedelta(hours=6) ):


    alreadyExists = await otp_collection.find_one({"shipment_id":str(id)})
    if(alreadyExists):
        await otp_collection.delete_one({"shipment_id":str(id)})

    await otp_collection.insert_one({
        "shipment_id":str(id),
        "otp":otp,
        "exp":datetime.now(tz=timezone.utc) + expiry
    })

async def _get_shipment_verfication_otp(id:UUID):

    shipment = await otp_collection.find_one({"shipment_id":str(id)})

    if not shipment:
        return None
    
    return shipment["otp"]

async def verify_shipment_verfication_otp(id:UUID,otp:int):
    shipment_otp = await _get_shipment_verfication_otp(id)

    if shipment_otp == otp:
        return True
    else:
        return False
