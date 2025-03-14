from redis import asyncio as redis

from app.settings import settings

if settings.TESTING == 'True':
    def get_redis_connection() -> redis.Redis:
        return redis.Redis(
            host=settings.CACHE_HOST,
            port=settings.CACHE_PORT,
            db=settings.CACHE_DB,
            decode_responses=True
        )
else:
    def get_redis_connection() -> redis.Redis:
        return redis.Redis(
            host=settings.CACHE_HOST,
            port=settings.CACHE_PORT,
            db=settings.CACHE_DB,
            decode_responses=True
        )
