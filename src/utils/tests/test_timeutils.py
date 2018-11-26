#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from library.test.unit.base import BaseTestCase
from library.utils.timeutils import TimeUtils
from datetime import datetime, date


class TimeUtilsTestCase(BaseTestCase):
    """
    测试时间模块
    """
    def setUp(self):
        self.time_utils = TimeUtils()

    def tearDown(self):
        pass

    def test_date2str(self):
        _date = date(2018, 04, 13)
        result = self.time_utils.date2str(_date)
        self.assertEquals(result, '2018-04-13')
