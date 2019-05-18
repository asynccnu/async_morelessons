import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_HOST = os.getenv('MONGODB_HOST') or 'localhost'
MONGODB_PORT = int(os.getenv('MONGODB_PORT') or '27017')
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME') or "muxi"
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD') or "nopassword"
LESSONSET = os.getenv('LESSONSET')
LESSONDB = os.getenv('LESSONDB')


async def db_setup():
    # client = AsyncIOMotorClient(MONGODB_HOST, MONGODB_PORT)
    mongo_uri = "mongodb://{}:{}@{}:{}".format(MONGODB_USERNAME, MONGODB_PASSWORD, MONGODB_HOST, MONGODB_PORT)
    client = AsyncIOMotorClient(mongo_uri)
    lessonset = client[LESSONSET]
    lessondb = lessonset[LESSONDB]
    return lessondb
