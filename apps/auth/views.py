"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:22
"""
from datetime import datetime, timedelta
from fastapi import Depends, APIRouter, Response
from fastapi.security import OAuth2PasswordRequestForm

from conf.logger import Logger
from lib.fastapi.error import ClientError
from .serializers import UserRetriveSerializer, TokenSerializer
from .settings import JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_AUTH_COOKIE
from .utils import authenticate_user, create_access_token, get_current_active_user

logger = Logger.get_logger(__name__)

router = APIRouter()


@router.post(
    "/token",
    response_model=TokenSerializer,
    summary="Login authentication",
    description="Login authentication",
    response_description="Login authentication",
)
async def login_for_access_token(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        logger.info(f'invalid user_auth: {form_data.username}')
        raise ClientError.BadRequest400('Perhaps username and/or password is incorrect.')
    access_token_expires = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    if JWT_AUTH_COOKIE:
        expiration = (datetime.utcnow() + access_token_expires)
        coockie_access_token = f"Bearer {access_token.decode('utf-8')}"
        response.set_cookie(key=JWT_AUTH_COOKIE,
                            value=coockie_access_token,
                            expires=expiration,
                            httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/users/me",
    response_model=UserRetriveSerializer,
    summary="Get current user information.",
    description="Get current user information.",
    response_description="Get current user information.",
)
async def read_users_me(
        current_user: UserRetriveSerializer = Depends(get_current_active_user)
):
    return current_user
