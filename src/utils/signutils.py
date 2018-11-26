#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import urllib

from library.utils.encodeutils import EnCodeUtils


class SignatureUtils(object):
    """
    签名 utils
    """
    def __init__(self, encoding='utf-8'):
        self.encoding = encoding

    def sort_param(self, params):
        for key, value in params.iteritems():
            print key, value
        sort_param = sorted([(key, EnCodeUtils().safe_encode(value, encoding=self.encoding))
                             for key, value in params.iteritems()], key=lambda x: x[0])
        content = '&'.join(['='.join(x) for x in sort_param])

        return content

    @staticmethod
    def url_encode(value):
        if value:
            return urllib.quote_plus(EnCodeUtils().safe_encode(value))

        return ''
