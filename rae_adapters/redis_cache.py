import os
from rae_core.interfaces.cache import ICacheProvider
from redis.asyncio import Redis

class RedisAdapter(ICacheProvider):
    def __init__(self, url: str = None, redis_client=None):
        self.url = url or os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self.client = redis_client or Redis.from_url(self.url)

    async def get(self, key: str):
        return await self.client.get(key)

    async def set(self, key: str, value: str, expire: int = None, ttl: int = None):
        await self.client.set(key, value, ex=expire or ttl)

    async def delete(self, key: str):
        await self.client.delete(key)
RedisCache = RedisAdapter
