"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:29
"""

import aioredis
from fastapi import FastAPI

from conf import settings
from conf.logger import Logger

logger = Logger.get_logger(__name__)


async def get_redis_connection(minsize=1, maxsize=1):
    redis = await aioredis.create_redis_pool(
        settings.REDIS_ADDRESS, password=settings.REDIS_PASSWORD, db=settings.REDIS_DB, minsize=minsize,
        maxsize=maxsize, encoding='utf-8')
    return redis


class Redis:
    redis = None

    @classmethod
    async def get_redis_connection(cls):
        if not cls.redis:
            cls.redis = await get_redis_connection(minsize=1, maxsize=100)
        return cls.redis

    @classmethod
    async def close(cls):
        if cls.redis:
            # gracefully closing underlying connection
            cls.redis.close()
            await cls.redis.wait_closed()
            cls.redis = None

    @classmethod
    def register(cls, app: FastAPI) -> None:

        @app.on_event("startup")
        async def startup() -> None:  # pylint: disable=W0612
            await cls.get_redis_connection()
            app.state._redis = cls.redis
            logger.info("Redis startup")

        @app.on_event("shutdown")
        async def shutdown() -> None:
            await cls.redis.close()
            logger.info("Redis shutdown")
