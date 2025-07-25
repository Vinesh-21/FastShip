from datetime import datetime, timedelta, timezone
import jwt

from fastapi import HTTPException, status

from app.config import security_settings

from uuid import uuid4

from app.database.mongodb import blacklist_collection

from datetime import datetime,timezone

# from rich import print

def genereate_access_token(data:dict,expiry:timedelta=timedelta(seconds=60)) -> str:
    return jwt.encode(
        payload={
                **data,
                "exp":datetime.now(timezone.utc) + expiry,
                "jti":str(uuid4())
            },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECERET_KEY
        )
    


async def decode_access_token(token: str)->dict:
    try:

        payload = jwt.decode(
            token,
            key=security_settings.JWT_SECERET_KEY,
            algorithms=[security_settings.JWT_ALGORITHM]
        )
    

        await check_user(payload["jti"])

        return payload
    except jwt.ExpiredSignatureError:

        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Invalid token signature")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token decoding failed")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while decoding the token: {str(e)}")
    

async def check_user(jti:str):
    jti = await blacklist_collection.find_one({"jti": jti})
    if jti:
        raise jwt.ExpiredSignatureError


async def invalidate_token(payload:dict):


    jti=payload["jti"]
    exp=datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    await blacklist_collection.insert_one({"jti":jti,"exp":exp})
    print("invalitadated user",payload["user"])



    