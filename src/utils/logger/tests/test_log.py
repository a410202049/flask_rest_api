#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from library.logger.log import init_logger_from_file, get_logger, init_logger_from_object

# init_logger_from_file('./logging.conf')


class Config(object):
    DEBUG = False
    LOG_PATH = 'log.log'

init_logger_from_object(Config())

logger = get_logger()
logger.info('12')
logger.debug('1')


