#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
# from __future__ import annotations

import time
from datetime import datetime, date
from library import logger


class TimeUtils(object):
    """
    时间相关的工具和辅助函数
    :parameter
    """
    def __init__(self, context=None):
        self.logger = context.logger if context and context.logger else logger.get_logger()

    def date2str(self, _date):
        """
        :type _date: date
        :return: date
        :cvar
        """
        result = _date.strftime('%Y%m%d')
        self.logger.debug('[{0}] convert to [{1}]'.format(_date, result))
        return result

    def str2date(self, input_str):
        result = datetime.strptime(input_str, '%Y%m%d').date()
        self.logger.debug('[{0}] convert to [{1}]'.format(input_str, result))
        return result

    def datetime2str(self, input_datetime):
        result = input_datetime.strftime('%Y%m%d%H%M%S')
        self.logger.debug('[{0}] convert to [{1}]'.format(input_datetime, result))
        return result

    def str2datetime(self, input_str):
        result = datetime.strptime(input_str, '%Y%m%d%H%M%S')
        self.logger.debug('[{0}] convert to [{1}]'.format(input_str, result))
        return result

    def timestamp_to_strtime(self, timestamp):
        if isinstance(timestamp, unicode):
            timestamp = float(timestamp)
        local_str_time = datetime.fromtimestamp(timestamp / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')
        self.logger.debug('[{0}] convert to [{1}]'.format(timestamp, local_str_time))
        return local_str_time

    def timestamp_to_datetime(self, timestamp):
        if isinstance(timestamp, unicode):
            timestamp = float(timestamp)
        local_dt_time = datetime.fromtimestamp(timestamp / 1000.0)
        self.logger.debug('[{0}] convert to [{1}]'.format(timestamp, local_dt_time))
        return local_dt_time

    def datetime_to_strtime(self, datetime_obj):
        local_str_time = datetime_obj.strftime("%Y-%m-%d %H:%M:%S.%f")
        self.logger.debug('[{0}] convert to [{1}]'.format(datetime_obj, local_str_time))
        return local_str_time

    def datetime_to_timestamp(self, datetime_obj):
        local_timestamp = long(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
        self.logger.debug('[{0}] convert to [{1}]'.format(datetime_obj, local_timestamp))
        return local_timestamp
