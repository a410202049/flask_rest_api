#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals


class FileUtils(object):
    """
    文件帮助工具
    """
    @staticmethod
    def read_all_data(file_path):
        with open(file_path, 'rU') as this_file:
            content = this_file.read()
        return content

    @staticmethod
    def read_by_lines(file_path):
        content = ''
        with open(file_path, 'rU') as this_file:
            for line in this_file.readlines():
                content += line.strip('\n')
        return content
