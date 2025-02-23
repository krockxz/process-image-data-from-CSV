from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_CONNECTION_STRING, DATABASE_NAME, COLLECTION_NAME

client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
db = client[DATABASE_NAME]
requests_collection = db[COLLECTION_NAME]
