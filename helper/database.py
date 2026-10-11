import motor.motor_asyncio
from config import DB_URL, DB_NAME
class WzgramDB:
    def __init__(self, uri, name):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
        self.db = self.client[name]
        self.col = self.db.users
    async def add_user(self, uid):
        if not await self.col.find_one({"_id": uid}):
            await self.col.insert_one({"_id": uid, "settings": {}})
    async def get_user_settings(self, uid):
        user = await self.col.find_one({"_id": uid})
        return user.get("settings", {}) if user else {}
    async def update_user_settings(self, uid, key, val):
        await self.col.update_one({"_id": uid}, {"$set": {f"settings.{key}": val}}, upsert=True)

db = WzgramDB(DB_URL, DB_NAME)
