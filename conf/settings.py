"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:29
"""

import os
import logging
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = config('FASTAPI_DEBUG', default=False, cast=bool)
if DEBUG:
    LOGGER_CONSOLE_LEVEL = logging.DEBUG
else:
    LOGGER_CONSOLE_LEVEL = logging.INFO

SECRET_KEY = config('API_SECRET', default='^=2p4poluvn4m(4_!wops2&$4*qth7qxgb-j@!4kuf6n%bs#2#')

PROJECT_CODE = 'DBLE'

API_PREFIX = config('API_PREFIX', default='api')

# redis settings
REDIS_HOST = config('REDIS_HOST', default='192.168.1.24')
REDIS_PORT = config('REDIS_PORT', default=6379, cast=int)
REDIS_PASSWORD = config('REDIS_PASSWORD', default='') or None
REDIS_DB = config('REDIS_DB', default=2, cast=int)
REDIS_ADDRESS = (REDIS_HOST, REDIS_PORT)

# RateThrottler settings
ARONYMOUS_THROTTLER_RATE = config('ARONYMOUS_THROTTLER_RATE', default="10/minute") or "60/minute"
AUTH_THROTTLER_RATE = config('AUTH_THROTTLER_RATE', default="10/minute") or "60/minute"

TIME_ZONE = 'UTC'

## 以下未使用
# mysql 配置
DB_HOST = config('DB_HOST', default='192.168.1.24')
DB_PORT = config('DB_PORT', default=3306, cast=int)
DB_USER = config('DB_USER', default='root')
DB_PASSWORD = config('DB_PASSWORD', default='123456')
DB_NAME = config('DB_NAME', default='dbo_track')
DB_ECHO = config('DB_ECHO', default=False, cast=bool)

TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': DB_HOST,
                'port': DB_PORT,
                'user': DB_USER,
                'password': DB_PASSWORD,
                'database': DB_NAME,
                'echo': DB_ECHO,
                "charset": "utf8mb4",
                "minsize": 1,
                "maxsize": 50,
            }
        },
    },
    'apps': {
        'models': {
            'models': ['apps.auth.models', 'apps.blog.models'],
            'default_connection': 'default',
        },
    },
}

# jwt 设置
JWT_SECRET_KEY = SECRET_KEY
JWT_ALGORITHM = config('JWT_ALGORITHM', default="HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = config('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', default=60 * 24 * 1, cast=int)
JWT_AUTH_COOKIE = config('JWT_AUTH_COOKIE', default="lvt_token")
