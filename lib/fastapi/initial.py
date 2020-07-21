"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:29
"""

import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from starlette.responses import JSONResponse

from .error import FastapiError
from .status import Http


def init_fastapi(
        title: str,
        description: str,
        version: str,
        path_prefix: str,
        startup_cb: callable = None,
        shutdown_cb: callable = None,
        health_cb: callable = None,
) -> FastAPI:
    health_failed_file = '/tmp/health.failed'
    # get_redoc_html.__kwdefaults__['redoc_favicon_url'] = '/static/images/logo.png'
    # get_swagger_ui_html.__kwdefaults__['swagger_favicon_url'] = '/static/images/logo.png'

    app = FastAPI(
        title=title,
        description=description,
        version=version,
        openapi_url=f'/{path_prefix}/openapi.json',
        docs_url=f'/{path_prefix}/docs',
        redoc_url=f'/{path_prefix}/redoc',
        swagger_ui_oauth2_redirect_url=f'/{path_prefix}/docs/oauth2-redirect',
    )

    @app.on_event("startup")
    async def startup():
        if startup_cb:
            await startup_cb()

    @app.on_event("shutdown")
    async def shutdown():
        if shutdown_cb:
            await shutdown_cb()

    @app.exception_handler(FastapiError)
    async def model_error_handler(_, exc: FastapiError):
        return JSONResponse(
            status_code=exc.code,
            content={
                "error": exc.name,
                "code": exc.code,
                "message": exc.msg,
            },
        )

    @app.exception_handler(AssertionError)
    async def model_error_handler(_, exc: AssertionError):
        logging.exception(exc)
        with open(health_failed_file, 'w+') as output:
            output.write(str(exc))
        return JSONResponse(
            status_code=Http.STATUS_500_INTERNAL_SERVER_ERROR.value,
            content={
                "error": Http.STATUS_500_INTERNAL_SERVER_ERROR.name,
                "code": Http.STATUS_500_INTERNAL_SERVER_ERROR.value,
                "message": f'Internal server error: {str(exc)}',
            },
        )

    @app.get("/ping", include_in_schema=False)
    async def ping():
        if os.path.isfile(health_failed_file):
            raise HTTPException(status_code=500, detail="Service failed")
        if health_cb and not await health_cb():
            raise HTTPException(status_code=503, detail="Service not healthy")
        return {"message": "pong"}

    return app
