import redis.asyncio as redis
from datetime import datetime, timezone

async def get_redis_client():
    client = redis.from_url(
        "redis://default:2CmS1BFmNyqgdVXvtRXRK79iW0WkRoBU@redis-15566.c244.us-east-1-2.ec2.redns.redis-cloud.com:15566",
        decode_responses=True
    )
    pong = await client.ping()
    print(f"Redis status: {pong} at {datetime.now(timezone.utc).isoformat()}")
    return client