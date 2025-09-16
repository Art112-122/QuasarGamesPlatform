import json
from typing import List, Dict
from databases.connection import get_redis_client


class RedisManager:
    def __init__(self):
        self.redis_client = None

    async def connect(self):
        self.redis_client = await get_redis_client()
        return self

    async def save_message(self, room_id: str, message: Dict):
        key = f"chat:{room_id}"
        await self.redis_client.rpush(key, json.dumps(message))
        await self.redis_client.ltrim(key, -100, -1)

    async def get_message_history(self, room_id: str) -> List[Dict]:
        key = f"chat:{room_id}"
        messages = await self.redis_client.lrange(key, 0, -1)
        return [json.loads(msg) for msg in messages]

    async def close(self):
        if self.redis_client:
            await self.redis_client.close()