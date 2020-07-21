"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:22
"""

import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, Request

from lib.fastapi.throttling import allow_request
from lib.fastapi.error import ClientError
from conf.settings import AUTH_THROTTLER_RATE
from .models import User as UserModel
from .settings import JWT_SECRET_KEY, JWT_ALGORITHM
from .oauth2 import oauth2_scheme
from .serializers import UserRetriveSerializer


async def authenticate_user(username: str, password: str):
    user = await UserModel.verify_login(username, password)
    if user and user.is_active:
        return user
    return None


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = ClientError.Unauthorized401("Could not validate credentials")
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = await UserModel.get_user(username)
    if user is None:
        raise credentials_exception
    return user


api_user_auth = get_current_user


async def get_current_active_user(user: UserRetriveSerializer = Depends(api_user_auth)):
    if not user.is_active:
        raise ClientError.BadRequest400("Inactive user")
    return user


async def auth_allow_request(request: Request, user: UserRetriveSerializer = Depends(get_current_active_user)):
    """ 登陆之后的访问限速
    """
    rate = AUTH_THROTTLER_RATE
    if not await allow_request(redis=request.app.state._redis,
                               scope=f"(user:{user.id})",
                               rate=rate,
                               host=request.client.host,
                               method=request.method,
                               url=request.url.path):
        e = f"Requests are too frequent, only can request {rate}"
        raise ClientError.BadRequest400(e)
    return user
