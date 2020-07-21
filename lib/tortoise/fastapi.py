"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:29
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from tortoise.exceptions import DoesNotExist, IntegrityError


def register_tortoise_exception(
        app: FastAPI,
        add_exception_handlers: bool = False,
) -> None:
    """ rewrite from tortoise.contrib.fastapi import register_tortoise
    """
    if add_exception_handlers:
        @app.exception_handler(DoesNotExist)
        async def doesnotexist_exception_handler(request: Request, exc: DoesNotExist):
            return JSONResponse(status_code=404, content={
                "error": "STATUS_404_NOT_FOUND",
                "code": 404,
                "message": str(exc)
            })

        @app.exception_handler(IntegrityError)
        async def integrityerror_exception_handler(request: Request, exc: IntegrityError):
            return JSONResponse(
                status_code=422,
                content={"detail": {"loc": [], "msg": str(exc), "type": "IntegrityError"}},
            )
