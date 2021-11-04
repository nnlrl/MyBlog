#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author    : nnlrl
# Created   : 2021/11/04
# Title     : mc.py
# Objective :
import inspect
import asyncio

from pickle import dumps, loads
from functools import wraps

from .utils import get_redis, Empty


def gen_key_factory(key_pattern: str, arg_names: list, kwonlydefaults: dict):
    def gen_key(*args, **kwargs):
        kw = kwonlydefaults.copy() if kwonlydefaults is not None else {}
        kw.update(zip(arg_names, args))
        kw.update(kwargs)
        if callable(key_pattern):
            key = key_pattern(*[kw[name] for name in arg_names])
        else:
            key = key_pattern.format(*[kw[n] for n in arg_names], **kw)
        return key and key.replace(' ', '_'), kw
    return gen_key


def cache(key_pattern):
    def deco(f):
        rv = inspect.getfullargspec(f)
        arg_names, kwonlydefaults = rv.args, rv.kwonlydefaults
        gen_key = gen_key_factory(key_pattern, arg_names, kwonlydefaults)

        @wraps(f)
        async def _(*args, **kwargs):
            redis = await get_redis()
            key, args = gen_key(*args, **kwargs)

            if not key:
                return f(*args, **kwargs)
            r = await redis.get(key)

            if r is None:
                r = await f(*args, **kwargs)
                if r is not None and not isinstance(r, Empty):
                    r = dumps(r)
                    await redis.set(key, r)
            else:
                print('Get from Cache...')
            try:
                r = loads(r)
            except TypeError:
                ...
            return r
        _.original_function = f
        return _
    return deco


async def clear_mc(*keys):
    redis = await get_redis()
    print(f'Clear cached: {keys}')
    assert redis is not None
    await asyncio.gather(*[redis.delete(k) for k in keys],
                         return_exceptions=True)
