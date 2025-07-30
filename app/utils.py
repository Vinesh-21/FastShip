from datetime import datetime, timedelta, timezone
from pathlib import Path
import jwt

from fastapi import HTTPException, status

from app.config import security_settings

from uuid import uuid4

from app.database.mongodb import blacklist_collection


APP_DIR = Path(__file__).resolve().parent

TEMPLATE_DIR = APP_DIR/"templates"


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



    