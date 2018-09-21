#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis
client = None

config = dict(
    REDIS_CACHES=None
)

def init_app(app):

    config['REDIS_CACHES'] = app.config.get('REDIS_CACHES', None)
    connection_pool = redis.ConnectionPool(**config['REDIS_CACHES'])

    global client
    client = redis.Redis(connection_pool=connection_pool)


def get_client():
    return client
