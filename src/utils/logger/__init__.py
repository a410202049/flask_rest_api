#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from .log import init_logger_from_file, init_logger_from_object, get_logger

__all__ = (
    'init_logger_from_file',
    'init_logger_from_object',
    'get_logger',
)
