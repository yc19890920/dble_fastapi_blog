"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:29
"""

from fastapi.responses import UJSONResponse
from fastapi import APIRouter, Query
from tortoise.transactions import in_transaction

from conf.logger import Logger
from lib.fastapi.error import ClientError
from lib.tortoise import pydantic_queryset_to_json

from .models import Tag, Category, Article
from .serializers import (
    TagCreateRequest, TagCreateResponse, TagListSerializer, TagListResponse,
    CategoryCreateRequest, CategoryCreateResponse, CategoryListSerializer, CategoryListResponse,
    ArticleCreateRequest, ArticleCreateResponse, ArticleListResponse, ArticleListSerializer
)

logger = Logger.get_logger(__name__)
router = APIRouter()


# ---- Tag ----
@router.post(
    "/tag",
    response_model=TagCreateResponse,
    summary="Tag create",
    description="Tag create",
    response_description="Tag Instance")
async def tag_create(data: TagCreateRequest):
    instance = await Tag.create(**data.dict(exclude_unset=True))
    return await TagCreateResponse.from_tortoise_orm(instance)


@router.patch(
    "/tag/{pk}",
    response_model=TagCreateResponse,
    summary="Tag update",
    description="Tag update",
    response_description="Tag Instance",
    responses={
        **ClientError.Unauthorized401('not authorized').response,
        **ClientError.NotFound404('Tag not Found').response,
    })
async def tag_update(pk, data: TagCreateRequest):
    instance = await Tag.get(id=pk)
    instance.update_from_dict(data.dict(exclude_unset=True))
    await instance.save()
    return await TagCreateResponse.from_tortoise_orm(instance)


@router.get(
    "/tag",
    response_model=TagListResponse,
    summary="Tag List",
    description="Tag List",
    response_description="Tag List",
    responses={
        **ClientError.Unauthorized401('not authorized').response,
    })
async def tag_list(index: int = Query(1, ge=1, description="page，default 1"),
                   limit: int = Query(10, ge=1, le=100, description="page_size，default 10")):
    qs = Tag.all()
    total = await qs.count()
    qs = qs.limit(limit).offset((index - 1) * limit)
    results = await TagListSerializer.from_queryset(qs)
    return UJSONResponse({
        "index": index,
        "limit": limit,
        "total": total,
        "results": pydantic_queryset_to_json(results)
    })


# ---- Category ----
@router.post(
    "/category",
    response_model=CategoryCreateResponse,
    summary="Category create",
    description="Category create",
    response_description="Category Instance")
async def category_create(data: CategoryCreateRequest):
    async with in_transaction(connection_name=Category.get_connection_name()):
        if await Category.filter(name=data.name).exists():
            raise ClientError.BadRequest400("Category name exist")
        instance = await Category.create(**data.dict(exclude_unset=True))
    return await CategoryCreateResponse.from_tortoise_orm(instance)


@router.patch(
    "/category/{pk}",
    response_model=CategoryCreateResponse,
    summary="Category update",
    description="Category update",
    response_description="Category Instance",
    responses={
        **ClientError.Unauthorized401('not authorized').response,
        **ClientError.NotFound404('Category not Found').response,
    })
async def category_update(pk, data: CategoryCreateRequest):
    instance = await Category.get(id=pk)
    instance.update_from_dict(data.dict(exclude_unset=True))
    await instance.save()
    return await CategoryCreateResponse.from_tortoise_orm(instance)


@router.get(
    "/category",
    response_model=CategoryListResponse,
    summary="Category List",
    description="Category List",
    response_description="Category List",
    responses={
        **ClientError.Unauthorized401('not authorized').response,
    })
async def category_list(index: int = Query(1, ge=1, description="page，default 1"),
                        limit: int = Query(10, ge=1, le=100, description="page_size，default 10")):
    qs = Category.all()
    total = await qs.count()
    qs = qs.limit(limit).offset((index - 1) * limit)
    results = await CategoryListSerializer.from_queryset(qs)
    return UJSONResponse({
        "index": index,
        "limit": limit,
        "total": total,
        "results": pydantic_queryset_to_json(results)
    })


# ---- Article ----
@router.post(
    "/article",
    response_model=ArticleCreateResponse,
    summary="Article create",
    description="Article create",
    response_description="Article Instance")
async def article_create(data: ArticleCreateRequest):
    async with in_transaction("default"):
        if not await Category.filter(id=data.category_id).exists():
            raise ClientError.BadRequest400(f"category_id({data.category_id}) not exist")
        for tag_id in data.tags:
            if not await Tag.filter(id=tag_id).exists():
                raise ClientError.BadRequest400(f"tag_id({tag_id}) not exist")
        tags = data.tags
        article__kwargs = data.dict()
        del article__kwargs['tags']
        instance = await Article.create(**article__kwargs)
        await instance.tags.add(*[
            await Tag.get(id=tag_id) for tag_id in list(set(tags))
        ])
    return await ArticleCreateResponse.from_tortoise_orm(instance)


@router.put(
    "/article/{pk}",
    response_model=ArticleCreateResponse,
    summary="Article update",
    description="Article update",
    response_description="Article Instance",
    responses={
        **ClientError.Unauthorized401('not authorized').response,
        **ClientError.NotFound404('Article not Found').response,
    })
async def article_update(pk, data: ArticleCreateRequest):
    async with in_transaction(connection_name=Article.get_connection_name()):
        if not await Category.filter(id=data.category_id).exists():
            raise ClientError.BadRequest400(f"category_id({data.category_id}) not exist")
        for tag_id in data.tags:
            if not await Tag.filter(id=tag_id).exists():
                raise ClientError.BadRequest400(f"tag_id({tag_id}) not exist")
        tags = data.tags
        article__kwargs = data.dict()
        del article__kwargs['tags']
        instance = await Article.get(id=pk)
        instance.update_from_dict(article__kwargs)
        await instance.save()
        await instance.tags.clear()
        await instance.tags.add(*[await Tag.get(id=tag_id) for tag_id in list(set(tags))])
    return await ArticleCreateResponse.from_tortoise_orm(instance)


@router.get(
    "/article",
    response_model=ArticleListResponse,
    summary="Article List",
    description="Article List",
    response_description="Article List",
    responses={
        **ClientError.Unauthorized401('not authorized').response,
    })
async def article_list(index: int = Query(1, ge=1, description="page，default 1"),
                       limit: int = Query(10, ge=1, le=100, description="page_size，default 10")):
    qs = Article.all()
    total = await qs.count()
    qs = qs.limit(limit).offset((index - 1) * limit)
    results = await ArticleListSerializer.from_queryset(qs)
    return UJSONResponse({
        "index": index,
        "limit": limit,
        "total": total,
        "results": pydantic_queryset_to_json(results)
    })
