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
    LOG_PATH = '/var/log/micro-service/src.log'
    UPLOAD_TEMP_PATH = './temp_file/'
    SERVICE_NAME = 'api_service'
    SERVICE_VERSION = 'v1.0.44'
    HOSTNAME = platform.node()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    SWAGGER_PATH = '/swagger'

    RESTPLUS_VALIDATE = True

    def __init__(self):
        self.CONFIG_NAME = self.get_config_name()

    def get_config_name(self):
        return self.__class__.__name__


class LocalConfig(DefaultConfig):
    DEBUG = False
    SQLALCHEMY_ECHO = True
    LOG_PATH = './src.log'

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