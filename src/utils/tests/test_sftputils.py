#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from test.unit.base import BaseTestCase
from utils.sftputils import SftpConnection


class SftpUtilsTestCase(BaseTestCase):
    """
    SftpUtilsTestCase
    tar -zcvf - 20180503_623185009100026951_000001.JPG 20180503_623185009100026951_000002.JPG|openssl enc -des3 -k 132e8a57b4f6139b3a5de9g4 -out IMGDOC0001_AXF_20180503_0001.zip
    openssl enc -des3 -k 132e8a57b4f6139b3a5de9g4 -d -in IMGDOC0001_AXF_20180503_0001.zip|tar -zxvf -
    openssl enc -des3 -k 132e8a57b4f6139b3a5de9g4 -d -in IMGDOC0001_AWX_20170724_0002.zip|tar -zxvf -
    https://nanjishidu.me/2017/10/openssl-enc.html
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_upload_file(self):
        pass

    def test_upload_data(self):
        with SftpConnection('sftp.zhihuianxin.com', 2201, 'bosc', 'XGrDsM1tUQy7kAjp') as connection:
            # index_result = connection.put('./IMGDOC0001_AXF_20180507_0001.txt', './shared/audio_visual_file/IMGDOC0001_AXF_20180507_0001.txt')
            # data_result = connection.put('./IMGDOC0001_AXF_20180503_0001.zip', './shared/audio_visual_file/IMGDOC0001_AXF_20180503_0001.zip')
            # print index_result, data_result
            dirs = connection.listdir('/home/bosc/profit_files/')
            w = connection.get('/home/bosc/profit_files/J_CBIB0020_AXF_20180729.zip', './3.zip')
            print dirs
