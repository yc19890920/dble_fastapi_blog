"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:29
"""
import time
import uuid
import math


class Locker:
    _acquire_digest = None
    __acquire_lua__ = """
    local key, identify, timeout = KEYS[1], ARGV[1], tonumber(ARGV[2])
    local ident, ret

    ident = redis.call('GET', key)
    if not ident then
        --  设置过期时间锁
        redis.call('SET', key, identify)
        redis.call('EXPIRE', key, timeout)
        ret = identify
    else
        --  未过期时间，则增加过期时间
        if redis.call('ttl', key) < 0 then
            redis.call('expire', key, timeout)
        end
        ret = nil
    end
    return ret
    """
    _release_digest = None
    __release_lua__ = """
    if redis.call('get', KEYS[1]) == ARGV[1] then
        return redis.call('del', KEYS[1]) or true
    end
    """

    @classmethod
    async def acquire(cls, redis, lockname, lock_timeout=30):
        identify = str(uuid.uuid4())
        lockname = 'lock:' + lockname
        # 确保传给EXPIRE的都是整数
        lock_timeout = int(math.ceil(lock_timeout))
        if not cls._acquire_digest:
            cls._acquire_digest = await redis.script_load(cls.__acquire_lua__)
        return await redis.evalsha(cls._acquire_digest, keys=[lockname], args=[identify, lock_timeout])
        # return await redis.evalsha(cls._acquire_digest, 1, *[lockname, identify, lock_timeout])

    @classmethod
    async def release(cls, redis, lockname, identify):
        if not cls._release_digest:
            cls._release_digest = await redis.script_load(cls.__release_lua__)
        return bool(
            await redis.evalsha(cls._release_digest, keys=["lock:" + lockname], args=[identify])
            # await redis.evalsha(cls._release_digest, 1, *["lock:" + lockname, identify])
        )

    @classmethod
    async def release_force(cls, redis, lockname):
        lockname = "lock:" + lockname
        return await redis.delete(lockname)


class RateThrottler:
    """
    from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
    """
    _digest = None
    __lua__ = """
    local key = KEYS[1]
    -- now 当前时间
    -- duration 时间间隔
    -- num_requests 最大多少个请求
    local now, duration, num_requests = tonumber(ARGV[1]), tonumber(ARGV[2]), tonumber(ARGV[3])
    
    -- h：历史time cjson字符串(列表字符串)
    -- t: time table
    local h, t
    h = redis.call('get', key)
    if h then
        t = cjson.decode(h)
    else
        t = {}
    end
    
    -- 删除历史数据
    for i=#t,1,-1 do
        if t[i] <= now - duration then
            table.remove(t, i)
        end
    end
    
    -- 是否超过限制
    if #t >= num_requests then
        return false
    end
    
    -- 可以正常访问, 设置time
    table.insert(t, now)
    redis.call('set', key, cjson.encode(t))
    -- 设置过期（可以考虑不过期也行）
    redis.call('expire', key, duration)
    return true
    """

    @classmethod
    async def allow_request(cls, redis, scope="anon", ident=None, rate=None):
        """ 可以用作网页访问限流器，或者登陆过频限制等
        :param redis:
        :param scope: anon/user/login
        :param ident: identifiter
        :param rate:  限速器， 5/seconds、5/m、5/h、5/day
        :return:
        """
        # 'throttle_%(scope)s_%(ident)s'  scope: anon or user  ident:  f"{self.host},{self.method},{self.url}"
        key = 'throttle_%(scope)s_%(ident)s' % {
            'scope': scope,
            'ident': ident
        }
        if rate is None:
            return True
        num_requests, duration = cls.parse_rate(rate)
        now = time.time()
        if not cls._digest:
            cls._digest = await redis.script_load(cls.__lua__)
        return await redis.evalsha(cls._digest, keys=[key], args=[now, duration, num_requests])

    @classmethod
    def parse_rate(cls, rate):
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>
        eg:
            5/day
            5/seconds
        """
        if rate is None:
            return (None, None)
        num, period = rate.split('/')
        num_requests = int(num)
        duration = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[period[0]]
        return (num_requests, duration)
