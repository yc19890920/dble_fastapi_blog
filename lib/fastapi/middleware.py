"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:42
"""
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


def register_fastapi_middleware(
        app: FastAPI,
        add_process_time_header: bool = False,
        add_corsmiddleware: bool = False,
):
    """
    :param app:
    :param add_process_time_header:
    :return:
    """
    if add_process_time_header:
        @app.middleware("http")
        async def add_process_time_header(request: Request, call_next):
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return response
    if add_corsmiddleware:
        app.add_middleware(CORSMiddleware,
                           allow_origins=["*"],
                           allow_credentials=True,
                           allow_methods=["*"],
                           allow_headers=["*"])
