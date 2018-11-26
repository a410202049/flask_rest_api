#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging
from logging import config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
        'network_formatter': {
            'format': '[%(levelname)1.1s]'
                      '[tm:%(asctime)s]'
                      '[pt:%(process)d:%(thread)d]'
                      '[file:%(module)s:%(lineno)d]'
                      '[app_name:%(app_name)s]'
                      '%(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'rotate_file': {
            'level': 'INFO',
            'class': 'library.logger.handlers.TimedRotatingFileHandler.TimedRotatingFileHandler',
            'filename': 'unit_test.log',
            'when': 'midnight',
            'interval': 1,  # day
            'backupCount': 7,
            'formatter': 'main_formatter',
        },
        'service_logger_file': {
            'level': 'INFO',
            'class': 'library.logger.handlers.TimedRotatingFileHandler.TimedRotatingFileHandler',
            'filename': 'unit_test_action.log',
            'when': 'midnight',
            'interval': 1,  # day
            'backupCount': 7,
            'formatter': 'network_formatter',
        },
        'service_logger_file_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'network_formatter',
            # 'filters': ['require_local_true'],
        },
    },
    'loggers': {
        'default': {
            'handlers': ['rotate_file'],
            'level': 'INFO',
        },
        'service_logger': {
            'handlers': ['service_logger_file_console', 'service_logger_file'],
            'level': 'DEBUG',
        },
    }
}

config.dictConfig(LOGGING)
logger = logging.getLogger('service_logger')

extra = {'app_name': 'aop', 'app_name1': 'aop'}
logger = logging.LoggerAdapter(logger, extra)

logger.info('ss')
logger.debug('ss')
