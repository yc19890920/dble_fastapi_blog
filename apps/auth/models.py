"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:22
"""
from __future__ import annotations

from typing import Optional
from tortoise import fields, Model
from passlib.hash import md5_crypt


class User(Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=150, null=False, unique=True, description="用户名")
    password = fields.CharField(max_length=128, null=False, description="密码")
    email = fields.CharField(max_length=254, null=True, description="邮箱")
    first_name = fields.CharField(max_length=30, null=True, description="first name")
    last_name = fields.CharField(max_length=30, null=True, description="last name")
    is_superuser = fields.BooleanField(default=False, description="是否是超级用户")
    is_staff = fields.BooleanField(default=False, description="管理员")
    is_active = fields.BooleanField(default=True, description="账户启用")
    last_login = fields.DatetimeField(null=True, description="最后登录时间")
    date_joined = fields.DatetimeField(auto_now=True, description="最后登录时间")

    class Meta:
        table = "user"
        table_description = "用户表"

    def __str__(self):
        return self.username

    @classmethod
    async def get_user(cls, username: str) -> Optional[User]:
        user = await User.filter(username=username).first()
        if user and user.is_active:
            return user
        return None

    @staticmethod
    async def verify_login(username: str, password: str) -> Optional[User]:
        user = await User.filter(username=username).first()
        if user and user.check_password(password):
            return user
        return None

    def set_password(self, raw_password):
        self.password = md5_crypt.hash(raw_password)

    def check_password(self, raw_password, t_password=None):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        return md5_crypt.verify(raw_password, self.password) if not t_password else t_password == self.password
