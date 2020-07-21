"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:29
"""

from typing import Optional, Any, Union, Type
from tortoise.fields import Field
from tortoise.fields.data import JsonDumpsFunc, JsonLoadsFunc, JSON_DUMPS, JSON_LOADS
from .models import Model, Empty


class JSONField(Field, dict, list):  # type: ignore
    """
    JSON field.

    This field can store dictionaries or lists of any JSON-compliant structure.

    You can specify your own custom JSON encoder/decoder, leaving at the default should work well.
    If you have ``python-rapidjson`` installed, we default to using that,
    else the default ``json`` module will be used.

    ``encoder``:
        The custom JSON encoder.
    ``decoder``:
        The custom JSON decoder.

    """

    SQL_TYPE = "TEXT"
    indexable = False

    class _db_postgres:
        SQL_TYPE = "JSONB"

    def __init__(
            self,
            encoder: JsonDumpsFunc = JSON_DUMPS,
            decoder: JsonLoadsFunc = JSON_LOADS,
            **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder

    def to_db_value(
            self, value: Optional[Union[dict, list]], instance: "Union[Type[Model], Model]"
    ) -> Optional[str]:
        if isinstance(value, str):
            value = value.strip()
        return None if value in (None, '', {}, [], ()) else self.encoder(value)

    def to_python_value(
            self, value: Optional[Union[str, dict, list]]
    ) -> Optional[Union[dict, list]]:
        value = None if value in Empty else value
        return self.decoder(value) if isinstance(value, str) else value
