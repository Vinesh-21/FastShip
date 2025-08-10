from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from app.config import mongoDB_Settings
from pymongo import IndexModel, ASCENDING

# MongoDB URI
uri = mongoDB_Settings.MONGODBURI

### Mongo Client 
mongo_client  = AsyncIOMotorClient(uri, server_api=ServerApi('1'))

### DataBase
db = mongo_client.blacklisting_db

### Collections
blacklist_collection = db.invalid_tokens
otp_collection = db.otp_sms


### Connection To MongoDB
async def connect_to_MongoDB():
  try:
    print("Initializing Connection to MongoDB ")
    await mongo_client.admin.command("ping")
    print("Connectied to MongoDB!")


  except Exception as e:
    print("MongoDB Connection Failed due to ",e)

### Indexing For TTL based on After Expiry
async def create_TTL_Indexing():
    print("Creating TTL index for the blacklist collection...")
    ttl_index = IndexModel([("exp", ASCENDING)], expireAfterSeconds=0)
    await blacklist_collection.create_indexes([ttl_index])
    print("Blacklist TTL index created successfully.")

    print("Creating TTL index for the OTP collection...")
    ttl_index_otp = IndexModel([("exp", ASCENDING)], expireAfterSeconds=0)
    await otp_collection.create_indexes([ttl_index_otp])
    print("OTP TTL index created successfully.")