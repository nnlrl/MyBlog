#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author    : nnlrl
# Created   : 2021/11/04
# Title     : utils.py
# Objective :
import config
import asyncio
import aioredis

from .var import redis_var

_redis = None


class Empty:

    def __call__(self, *a, **kw):
        return empty

    def __nonzero__(self):
        return False

    def __contains__(self, item):
        return False

    def __repr__(self):
        return '<Empty Object>'

    def __str__(self):
        return ''

    def __eq__(self, v):
        return isinstance(v, Empty)

    def __len__(self):
        return 0

    def __getitem__(self, key):
        return empty

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration

    def next(self):
        raise StopIteration

    def __getattr__(self, mname):
        return ''

    def __setattr__(self, name, value):
        return self

    def __delattr__(self, name):
        return self

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d


empty = Empty()


async def get_redis():
    global _redis
    if _redis is None:
        try:
            redis = redis_var.get()
        except LookupError:
            # Hack for debug mode
            loop = asyncio.get_event_loop()
            redis = await aioredis.create_redis_pool(
                config.REDIS_URL, minsize=5, maxsize=20, loop=loop)
        _redis = redis
    return _redis

if __name__ == '__main__':
    redis = get_redis()
