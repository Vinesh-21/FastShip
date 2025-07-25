from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from app.config import mongoDB_Settings
from pymongo import IndexModel, ASCENDING


uri = mongoDB_Settings.MONGODBURI

mongo_client  = AsyncIOMotorClient(uri, server_api=ServerApi('1'))

db = mongo_client.blacklisting_db

blacklist_collection = db.invalid_tokens

async def connect_to_MongoDB():
  try:
    print("Initializing Connection to MongoDB ")
    await mongo_client.admin.command("ping")
    print("Connectied to MongoDB!")


  except Exception as e:
    print("MongoDB Connection Failed due to ",e)

async def create_TTL_Indexing():
    print("Creating TTL index for the blacklist collection...")
    blacklist_collection = db.invalid_tokens
    ttl_index = IndexModel([("exp", ASCENDING)], expireAfterSeconds=0)
    await blacklist_collection.create_indexes([ttl_index])
    print("TTL index created successfully.")