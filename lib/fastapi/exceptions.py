"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:29
"""

from typing import Union
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def http422_error_handler(
        _: Request, exc: Union[RequestValidationError, ValidationError,]
) -> JSONResponse:
    errors = exc.errors()
    for err in errors:
        message = "->".join(err['loc']) + ": " + err['msg']
        break
    else:
        message = errors
    return JSONResponse({
        "code": HTTP_422_UNPROCESSABLE_ENTITY,
        "message": message,
        "error": errors,
    }, status_code=HTTP_422_UNPROCESSABLE_ENTITY)


validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},
    }
}


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({
        "code": exc.status_code,
        "message": exc.detail,
        "error": exc.detail,
    }, status_code=HTTP_422_UNPROCESSABLE_ENTITY)


def register_fastapi_exception(app: FastAPI):
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)
