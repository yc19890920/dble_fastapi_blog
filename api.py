"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:42
"""

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from conf import settings
from conf.logger import Logger
from conf.settings import TORTOISE_ORM
from lib.redis.connect import Redis
from lib.tortoise import register_tortoise_exception
from lib.fastapi.error import ClientError
from lib.fastapi.initial import init_fastapi
from lib.fastapi.exceptions import register_fastapi_exception
from lib.fastapi.middleware import register_fastapi_middleware
from lib.fastapi.throttling import allow_request, anon_allow_request
from apps.auth.utils import api_user_auth, auth_allow_request
from apps.auth import views as auth_views
from apps.blog import views as blog_views

logger = Logger.get_logger(__name__)


def get_application() -> FastAPI:
    application = init_fastapi(
        title='Blog',
        description='Blog API.',
        version='0.0.1',
        path_prefix=settings.API_PREFIX,
        startup_cb=None,
        shutdown_cb=None,
    )
    register_fastapi_middleware(application, add_corsmiddleware=True, add_process_time_header=True)
    register_tortoise(application, config=TORTOISE_ORM, generate_schemas=False)
    register_tortoise_exception(application, add_exception_handlers=True)
    register_fastapi_exception(application)
    Redis.register(application)

    # 静态文件
    application.mount("/static", StaticFiles(directory="static"), name="static")

    application.include_router(
        blog_views.router,
        prefix=f"/{settings.API_PREFIX}/v1",
        tags=['Blog'],
        dependencies=[Depends(auth_allow_request)],
        responses={
            **ClientError.Unauthorized401('not authorized').response,
        },
    )

    application.include_router(
        auth_views.router,
        prefix=f"/{settings.API_PREFIX}/v1",
        tags=['JWT'],
        responses={
            **ClientError.Unauthorized401('not authorized').response,
        },
    )

    return application


app = get_application()
