"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:24
"""

import pytz

DT_FMT = "%Y-%m-%d %H:%M:%S"
D_FMT = "%Y-%m-%d"
TZ_FMT = "%Y-%m-%dT%H:%M:%SZ"

KB = 1 << 10
MB = 1 << 20
GB = 1 << 30
TB = 1 << 40
PB = 1 << 50

utc = pytz.utc

Empty = ('', None, dict(), list(), tuple())
