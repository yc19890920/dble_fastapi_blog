"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:22
"""

from typing import List
from pydantic import BaseModel, Field
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from lib.tortoise.pydantic import json_encoders
from .models import Tag, Category, Article

Tortoise.init_models(["apps.blog.models"], "models")


class PydanticResponse(BaseModel):
    index: int
    limit: int
    total: int


# -*- tag -*-
# Tag create/update
TagCreateRequest = pydantic_model_creator(
    Tag, name="TagCreateRequest", exclude_readonly=True
)

TagCreateResponse = pydantic_model_creator(
    Category, name="TagCreateResponse", exclude=["articles"]
)
TagCreateResponse.Config.json_encoders = json_encoders

# Tag List
TagListSerializer = pydantic_queryset_creator(
    Tag, name="TagListSerializer", exclude=["articles"]
)


class TagListResponse(PydanticResponse):
    results: List[TagListSerializer]


class TagResponse(BaseModel):
    id: int
    name: str


# -*- Category -*-
# Category create/update
CategoryCreateRequest = pydantic_model_creator(
    Category, name="CategoryCreateRequest", exclude_readonly=True
)

CategoryCreateResponse = pydantic_model_creator(
    Category, name="CategoryCreateResponse", exclude=("articles",)
)
CategoryCreateResponse.Config.json_encoders = json_encoders

# Category List
CategoryListSerializer = pydantic_queryset_creator(
    Category, name="CategoryListSerializer", exclude=("articles",)
)


class CategoryListResponse(PydanticResponse):
    results: List[CategoryListSerializer]


# -*- Article -*-
# Article create/update
class ArticleCreateRequest(BaseModel):
    title: str = Field(..., description="Title")
    content: str = Field(..., description="Content")
    abstract: str = None
    status: str = Field(default="publish", description="Content")
    category_id: int = Field(..., description="category_id")
    tags: List[int] = Field(..., description="tag_id list")


ArticleCreateResponse = pydantic_model_creator(
    Article, name="ArticleCreateResponse"
)
ArticleCreateResponse.Config.json_encoders = json_encoders

ArticleListSerializer = pydantic_queryset_creator(
    Article, name="ArticleListSerializer"
)


# Article List
class ArticleListResponse(PydanticResponse):
    results: List[ArticleCreateResponse]
