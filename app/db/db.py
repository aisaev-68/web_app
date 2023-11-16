from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings


async def get_db() -> AsyncIOMotorClient:
    try:
        db_client = AsyncIOMotorClient(
            settings.MONGO_URI,
            maxPoolSize=settings.MAX_CONNECTIONS_COUNT,
            minPoolSize=settings.MIN_CONNECTIONS_COUNT,
            uuidRepresentation="standard",
        )

        return db_client
    except Exception as e:
        print(f'Could not connect to mongo: {e}')
        raise
