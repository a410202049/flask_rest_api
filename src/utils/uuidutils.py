#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import uuid


class UUIDUtils(object):
    """
    uuid utils
    """
    @staticmethod
    def generate_uuid(dashed=True):
        """创建一个随机UUID字符串.
        :param dashed: 是否要破折号
        :type dashed: bool
        :returns: str
        """
        if dashed:
            return str(uuid.uuid4())
        return uuid.uuid4().hex

    @staticmethod
    def format_uuid_string(string):
        return (string.replace('urn:', '')
                .replace('uuid:', '')
                .strip('{}')
                .replace('-', '')
                .lower())

    def is_uuid_like(self, val):
        """判断uuid
        :param val: 验证的值
        :type val: str
        :returns: bool
        """
        try:
            return str(uuid.UUID(val)).replace('-', '') == self.format_uuid_string(val)
        except (TypeError, ValueError, AttributeError):
            return False
