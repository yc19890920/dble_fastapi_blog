"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:22
"""
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from .models import User

# User
UserRetriveSerializer = pydantic_model_creator(
    User, name="User",
    include=["id", "username", "email", "is_active", "is_staff", "last_login"])


# Token
class TokenSerializer(BaseModel):
    access_token: str
    token_type: str
