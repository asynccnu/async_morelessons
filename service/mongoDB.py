import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_HOST = os.getenv('MONGODB_HOST') or 'localhost'
MONGODB_PORT = int(os.getenv('MONGODB_PORT') or '27017')


async def db_setup():
    client = AsyncIOMotorClient(MONGODB_HOST, MONGODB_PORT)
    lessonset = client['lessonset2018']
    lessondb = lessonset['lessondb2018']
    return lessondb
