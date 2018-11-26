#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import sys
import six


class EnCodeUtils(object):
    """
    字符串编码解码工具类, string_escape, unicode_escape
    8个比特（bit）作为一个字节（byte）;
    unicode-escape， string-escape
    """
    @staticmethod
    def safe_decode(text, incoming=None, errors='strict'):
        """
        安全解码
        :param text: 输入的文本
        :param incoming: 编码
        :param errors:
        :return: 返回编码结果
        """
        if not isinstance(text, (six.string_types, six.binary_type)):
            raise TypeError("%s can't be decoded" % type(text))

        if isinstance(text, six.text_type):
            return text

        if not incoming:
            incoming = (sys.stdin.encoding or
                        sys.getdefaultencoding())

        try:
            s = text.decode(incoming, errors)
            print s
            return text.decode(incoming, errors)
        except UnicodeDecodeError:
            return text.decode('utf-8', errors)

    def safe_encode(self, text, incoming=None,
                    encoding='utf-8', errors='strict'):
        """
        安全编码
        :param text:
        :param incoming:
        :param encoding:
        :param errors:
        :return:
        """
        if not isinstance(text, (six.string_types, six.binary_type)):
            raise TypeError("%s can't be encoded" % type(text))

        if not incoming:
            incoming = (sys.stdin.encoding or
                        sys.getdefaultencoding())

        if hasattr(incoming, 'lower'):
            incoming = incoming.lower()
        if hasattr(encoding, 'lower'):
            encoding = encoding.lower()

        if isinstance(text, six.text_type):
            return text.encode(encoding, errors)
        elif text and encoding != incoming:
            text = self.safe_decode(text, incoming, errors)
            return text.encode(encoding, errors)
        else:
            return text

    @staticmethod
    def to_utf8(text):
        """Encode Unicode to UTF-8
        """
        if isinstance(text, six.binary_type):
            return text
        elif isinstance(text, six.text_type):
            return text.encode('utf-8')
        else:
            raise TypeError("bytes or Unicode expected, got %s"
                            % type(text).__name__)

    @staticmethod
    def exception_to_unicode(exc):
        """
        异常转为Unicode
        """
        msg = None
        if six.PY2:
            try:
                msg = unicode(exc)
            except UnicodeError:
                if hasattr(exc, '__unicode__'):
                    try:
                        msg = exc.__unicode__()
                    except UnicodeError:
                        pass

        if msg is None:
            msg = exc.__str__()

        if isinstance(msg, six.text_type):
            return msg

        try:
            return msg.decode('utf-8')
        except UnicodeDecodeError:
            pass

        encoding = sys.getfilesystemencoding()
        try:
            return msg.decode(encoding)
        except UnicodeDecodeError:
            pass

        return msg.decode('latin1')
