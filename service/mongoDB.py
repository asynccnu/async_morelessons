import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.environ.get("MONGO_URI") or "mongodb://username:secret@localhost:27017/?authSource=admin"

LESSONSET = os.getenv('LESSONSET')
LESSONDB = os.getenv('LESSONDB')


async def db_setup():
    # client = AsyncIOMotorClient(MONGODB_HOST, MONGODB_PORT)
    mongo_uri = MONGO_URI
    client = AsyncIOMotorClient(mongo_uri)
    lessonset = client[LESSONSET]
    lessondb = lessonset[LESSONDB]
    return lessondb
