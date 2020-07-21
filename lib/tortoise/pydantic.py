"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:29
"""

import ujson as json
from typing import Type, Any, Dict, Callable
from tortoise.contrib.pydantic.base import PydanticListModel, PydanticModel

import datetime
from pydantic import BaseModel
from pydantic.json import ENCODERS_BY_TYPE
from dataclasses import asdict, is_dataclass
from conf.constants import Empty, TZ_FMT

__ROOT__ = "__root__"


def isoformat_dt(dt: datetime.datetime = None) -> str:
    if dt in Empty:
        return None
    return dt.strftime(TZ_FMT)


ENCODERS_BY_TYPE: Dict[Type[Any], Callable[[Any], Any]] = {
    **ENCODERS_BY_TYPE,
    datetime.datetime: isoformat_dt,
}


def pydantic_encoder(obj: Any) -> Any:
    if isinstance(obj, BaseModel):
        return obj.dict()
    elif is_dataclass(obj):
        return asdict(obj)

    # Check the class type and its superclasses for a matching encoder
    for base in obj.__class__.__mro__[:-1]:
        try:
            encoder = ENCODERS_BY_TYPE[base]
        except KeyError:
            continue
        return encoder(obj)
    else:  # We have exited the for loop without finding a suitable encoder
        raise TypeError(f"Object of type '{obj.__class__.__name__}' is not JSON serializable")


json_encoders = {datetime.datetime: pydantic_encoder}


def pydantic_queryset_to_json(results: Type[PydanticListModel]):
    return json.loads(results.json(encoder=pydantic_encoder))


def pydantic_model_to_json(results: Type[PydanticModel]):
    return json.loads(results.json(encoder=pydantic_encoder))


def pydantic_queryset_to_dict(results: Type[PydanticListModel]):
    return results.dict()[__ROOT__]
