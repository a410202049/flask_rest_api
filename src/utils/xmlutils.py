#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import json
import xmltodict


class XMLUtils(object):
    """
    xml utils
    """
    @staticmethod
    def xml2json(xml_str, need_dict=False, encoding='utf-8'):
        """
        xml to json
        :return:
        """
        json_data = xmltodict.parse(xml_str, encoding=encoding)

        if need_dict:
            return json_data

        return json.dumps(json_data, indent=1, encoding=encoding)

    @staticmethod
    def json2xml(json_data, encoding='utf-8', full_document=True):
        """
        json to xml
        :param full_document:
        :param encoding:
        :param json_data:
        :return:
        """
        if not isinstance(json_data, dict):
            json_data = json.loads(json_data, encoding=encoding)

        xml_str = xmltodict.unparse(json_data, encoding=encoding, full_document=full_document)
        return xml_str
