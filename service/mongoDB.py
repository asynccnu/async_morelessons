import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_HOST = os.getenv('MONGOHOST') or 'localhost'
MONGODB_PORT = int(os.getenv('MONGOPORT') or '27017')


async def db_setup():
    client = AsyncIOMotorClient(MONGODB_HOST, MONGODB_PORT)
    lessonset = client['lessonset']
    lessondb = lessonset['lessondb']
    return lessondb
