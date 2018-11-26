#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from library.test.unit.base import BaseTestCase
from library.utils.encodeutils import EnCodeUtils


class EncodeTestCase(BaseTestCase):
    """
    测试 encode decode
    """
    def setUp(self):
        self.encode_utils = EnCodeUtils()

    def tearDown(self):
        pass

    def test_safe_decode(self):
        value = self.encode_utils.safe_decode(u'\u9ad8\u6e90')
        print value
