"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:29
"""

import ujson as json

__ROOT__ = "__root__"


class Cache:

    @classmethod
    async def set(cls, redis, key, value, expired=3600):
        if not value:
            return
        p = redis.pipeline()
        value = {__ROOT__: value}
        p.set(key, json.dumps(value))
        p.expire(key, expired)
        __ = await p.execute()

    @classmethod
    async def get(cls, redis, key):
        value = await redis.get(key)
        if value is None:
            return None
        return json.loads(value)[__ROOT__]
