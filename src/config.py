#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import platform
from datetime import timedelta

from celery.schedules import crontab

location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), x)


class DefaultConfig(object):
    DEBUG = False
    SECRET_KEY = '\x03d\xf4\x95J\x15\xa4B\xfb\xc0\xaf \xd1A[j$}\x18\x16a\xe7\xd0\xec'
    LOG_PATH = '/var/log/micro-service/src.log'
    UPLOAD_TEMP_PATH = './temp_file/'
    SERVICE_NAME = 'api_service'
    SERVICE_VERSION = 'v1.0.44'
    HOSTNAME = platform.node()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # JWT CONFIG
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ALGORITHM = 'HS256'

    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = ''
    # JWT_JSON_KEY = 'access_token'
    # JWT_REFRESH_JSON_KEY = 'refresh_token'

    # Email config
    MAIL_SERVER = 'xxx'
    MAIL_PORT = 1122
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'xxxx'
    MAIL_PASSWORD = 'xxx'

    # REDIS CONFIG
    REDIS_CACHES = {
        'host': '127.0.0.1',
        'port': '6379',
        'db': 0,
        'password': ''
    }

    NETWORK_FORMATTER = '[%(levelname)1.1s][%(method)s][tm:%(asctime)s][request_id:%(request_id)s]' \
                        '[file:%(module)s:%(funcName)s:%(lineno)d] %(message)s'
    SWAGGER_PATH = '/swagger'

    RESTPLUS_VALIDATE = True

    def __init__(self):
        self.CONFIG_NAME = self.get_config_name()

    def get_config_name(self):
        return self.__class__.__name__


class LocalConfig(DefaultConfig):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    # LOG_PATH = './src.log'

    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1/flask_base_plus?charset=utf8"
    DB_SESSION_OPTIONS = dict(autocommit=False, autoflush=False, expire_on_commit=False)

    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
    CELERY_BROKER_URL = 'redis://localhost:6379/1'

    CELERY_INCLUDE = [
        'task.income_task',
    ]

    CELERYBEAT_SCHEDULE = {
        'sync_income_info': {
            'task': 'task.income_task.sync_income_info',
            # 'schedule': crontab(second='*/5'),
            'schedule': timedelta(seconds=10),
        },
    }


class DevelopConfig(DefaultConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True

    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1/flask_base_plus?charset=utf8"
    DB_SESSION_OPTIONS = dict(autocommit=False, autoflush=False, expire_on_commit=False)

    CELERY_RESULT_BACKEND = 'redis://:a932tFl3@r-bp183abcb22d5b44.redis.rds.aliyuncs.com:6379/30'
    CELERY_BROKER_URL = 'redis://:a932tFl3@r-bp183abcb22d5b44.redis.rds.aliyuncs.com:6379/30'

    CELERY_INCLUDE = [
        'task.income_task',
    ]

    CELERYBEAT_SCHEDULE = {
        'sync_income_info': {
            'task': 'task.income_task.sync_income_info',
            # 'schedule': crontab(second='*/5'),
            'schedule': timedelta(seconds=10),
        },
    }


class OnlineConfig(DefaultConfig):
    DEBUG = False
    SQLALCHEMY_ECHO = False

    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1/flask_base_plus?charset=utf8"
    DB_SESSION_OPTIONS = dict(autocommit=False, autoflush=False, expire_on_commit=False)

    CELERY_RESULT_BACKEND = 'redis://:N7jpd0Hs@r-bp1103a711938674.redis.rds.aliyuncs.com:6379/25'
    CELERY_BROKER_URL = 'redis://:N7jpd0Hs@r-bp1103a711938674.redis.rds.aliyuncs.com:6379/25'

    CELERY_INCLUDE = [
        'task.income_task',
    ]

    CELERYBEAT_SCHEDULE = {
        'sync_income_info': {
            'task': 'task.income_task.sync_income_info',
            # 'schedule': crontab(second='*/5'),
            'schedule': timedelta(seconds=10),
        },
    }


CONFIGS = {
    'local': LocalConfig,
    'devel': DevelopConfig,
    'online': OnlineConfig,
}


def get_config(name):
    config_class = CONFIGS.get(name)
    if config_class:
        return config_class()
    else:
        raise Exception('unrecognized config name: %s' % name)
