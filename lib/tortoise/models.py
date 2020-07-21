"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:29
"""

from typing import (
    Any,
    Optional,
    Tuple,
    Type
)
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.models import Model, MODEL

Empty = ('', None, dict(), list(), tuple())


class Model(Model):

    @classmethod
    async def update_or_create(
            cls: Type[MODEL],
            defaults: Optional[dict] = None,
            using_db: Optional[BaseDBAsyncClient] = None,
            **kwargs: Any,
    ) -> Tuple[MODEL, bool]:
        if not defaults:
            defaults = {}
        for k, __ in kwargs.items():
            if k in defaults:
                del defaults[k]
        instance, _created = await cls.get_or_create(defaults, using_db, **kwargs)
        if not _created:
            for k, v in defaults.items():
                v = None if v in Empty else v
                setattr(instance, k, v() if callable(v) else v)
            await instance.save(using_db=using_db)
        return instance, _created
