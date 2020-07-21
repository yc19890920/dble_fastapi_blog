"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:29
"""

import time
from fastapi import Request

from lib.redis.cache import Cache
from lib.redis.lua import RateThrottler
from .error import ClientError
from conf.settings import ARONYMOUS_THROTTLER_RATE


class SimpleRateThrottle:
    cache_format = 'throttle_%(scope)s_%(ident)s'
    THROTTLE_RATES = {
        'anon': '100/day',
        'user': '1000/day'
    }
    scope = None
    timer = time.time

    def __init__(self, redis, rate=None, host=None, method=None, url=None):
        self.rate = rate
        if not rate:
            self.rate = self.get_rate()
        self.num_requests, self.duration = self.parse_rate(self.rate)
        self.cache = Cache
        self.redis = redis
        self.host = host
        self.method = method
        self.url = url

    def get_rate(self):
        """
        Determine the string representation of the allowed request rate.
        """
        try:
            return self.THROTTLE_RATES[self.scope]
        except KeyError:
            msg = "No default throttle rate set for '%s' scope" % self.scope
            raise ValueError(msg)

    def parse_rate(self, rate):
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>
        """
        if rate is None:
            return (None, None)
        num, period = rate.split('/')
        num_requests = int(num)
        duration = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[period[0]]
        return (num_requests, duration)

    def get_ident(self):
        return f"{self.host},{self.method},{self.url}"

    def get_cache_key(self):
        """
        Should return a unique cache-key which can be used for throttling.
        Must be overridden.

        May return `None` if the request should not be throttled.
        """
        raise NotImplementedError('.get_cache_key() must be overridden')

    async def allow_request(self):
        """
        Implement the check to see if the request should be throttled.

        On success calls `throttle_success`.
        On failure calls `throttle_failure`.
        """
        if self.rate is None:
            return True

        self.key = self.get_cache_key()
        if self.key is None:
            return True

        self.history = await self.cache.get(self.redis, self.key) or []
        self.now = self.timer()

        # Drop any requests from the history which have now passed the
        # throttle duration
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()

        if len(self.history) >= self.num_requests:
            return self.throttle_failure()
        return await self.throttle_success()

    async def throttle_success(self):
        """
        Inserts the current request's timestamp along with the key
        into the cache.
        """
        self.history.insert(0, self.now)
        await self.cache.set(self.redis, self.key, self.history, self.duration)
        return True

    def throttle_failure(self):
        """
        Called when a request to the API has failed due to throttling.
        """
        return False

    def wait(self):
        """
        Returns the recommended next request time in seconds.
        """
        if self.history:
            remaining_duration = self.duration - (self.now - self.history[-1])
        else:
            remaining_duration = self.duration

        available_requests = self.num_requests - len(self.history) + 1
        if available_requests <= 0:
            return None

        return remaining_duration / float(available_requests)


class AnonRateThrottle(SimpleRateThrottle):
    """
    Limits the rate of API calls that may be made by a anonymous users.

    The IP address of the request will be used as the unique cache key.
    """
    scope = 'anon'

    def get_cache_key(self):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident()
        }


async def throttling_any(redis, rate=None, host=None, method=None, url=None):
    t = AnonRateThrottle(redis=redis,
                         rate=rate,
                         host=host,
                         method=method,
                         url=url)
    return await t.allow_request()


async def allow_request(redis, scope="anon", rate=None, host=None, method=None, url=None):
    ident = f"{host},{method},{url}"
    return await RateThrottler.allow_request(redis, scope=scope, ident=ident, rate=rate)


async def anon_allow_request(request: Request):
    """ used as: dependencies=[Depends(auth_allow_request)],
    """
    rate = ARONYMOUS_THROTTLER_RATE
    if not await allow_request(redis=request.app.state._redis,
                               scope="anon",
                               rate=rate,
                               host=request.client.host,
                               method=request.method,
                               url=request.url.path):
        e = f"Requests are too frequent, only can request {rate}"
        raise ClientError.BadRequest400(e)
    return True
