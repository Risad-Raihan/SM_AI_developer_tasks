from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    async def connect_to_mongo(cls):
        MongoDB.client = AsyncIOMotorClient(settings.MONGODB_URL)
        MongoDB.db = MongoDB.client[settings.MONGODB_DB_NAME]
        print(f"Connected to MongoDB at {settings.MONGODB_URL}")

    @classmethod
    async def close_mongo_connection(cls):
        if MongoDB.client is not None:
            MongoDB.client.close()
            print("MongoDB connection closed")

    @classmethod
    def get_collection(cls, collection_name: str):
        # Initialize connection if not already done
        if MongoDB.client is None:
            # For synchronous access, create connection immediately
            MongoDB.client = AsyncIOMotorClient(settings.MONGODB_URL)
            MongoDB.db = MongoDB.client[settings.MONGODB_DB_NAME]
            print(f"Connected to MongoDB at {settings.MONGODB_URL}")
        
        return MongoDB.db[collection_name]

# Collections
conversations = MongoDB.get_collection("conversations")
menu_items = MongoDB.get_collection("menu_items")
reservations = MongoDB.get_collection("reservations")
restaurant_info = MongoDB.get_collection("restaurant_info") 