#!/usr/bin/python
# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import os
import uuid
import requests
from celery import Celery
import urllib, urllib2
import ssl
import base64
import json
import datetime
from Crypto.Cipher import DES3
from library.context.context import Context
from sqlalchemy import or_

from server.exception import BusinessException, INVALID_REQUEST_VALUE

from library.db_session import DBSessionForRead, DBSessionForWrite
import codecs
import zipfile
from library.utils.sftputils import SftpConnection
from decimal import Decimal
import traceback

celery = None


class BaseConfig(object):
    @classmethod
    def from_map(cls, mapping):
        prefix = getattr(cls, '__prefix__', '').upper()

        for k in cls.__dict__:
            if not 'k'.startswith('_') and k.isupper():
                k = prefix + k
                if k in mapping:
                    setattr(cls, k, mapping[k])

    @classmethod
    def from_obj(cls, obj):
        cls.from_map(obj.__dict__)


class Config(BaseConfig):
    VERSION = '1.0.0'
    SYS_API_INST = None


def make_celery(app):
    global celery
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    Config.from_map(app.config)
    return celery


if __name__ == '__main__':
    pass
