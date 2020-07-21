"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:22
"""

from tortoise import fields
from lib.tortoise.models import Model


class Tag(Model):
    name = fields.CharField(max_length=100, unique=True, description="名称")
    created = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = 'blog_tag'
        table_description = '标签'


class Category(Model):
    name = fields.CharField(max_length=100, unique=True, description="名称")
    created = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = 'blog_category'
        table_description = '标签'


class Article(Model):
    title = fields.CharField(max_length=100, index=True, description="主题")
    content = fields.TextField(null=True, description="内容")
    abstract = fields.TextField(null=True, description="摘要")
    status = fields.CharField(max_length=20, null=True, description="状态")
    tags: fields.ManyToManyRelation["Tag"] = fields.ManyToManyField(
        "models.Tag", related_name="articles", through="blog_article_tag"
    )
    category: fields.ForeignKeyRelation[Category] = fields.ForeignKeyField(
        "models.Category", related_name="articles", on_delete=fields.SET_NULL, null=True, to_field="id"
    )
    created = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = 'blog_article'
        table_description = '标签'
