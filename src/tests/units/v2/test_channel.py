#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import json

from server.resource.v2.channel.channels import GTChannel, ALYChannel
from tests.units import BaseTestCase


class GTChannelTestCase(BaseTestCase):
    """
    个推通道测试
    """
    def setUp(self):
        self.gt_channel = GTChannel(self.ctx, 'fdb3509f076048a0af4a2d63eb2ee40d','GTChannel', 'GTChannel' ,'http://sdk.open.api.igexin.com/apiex.htm', 1)
        self.gt_channel.app_id = '9CTEzxXUb78YbMfUHZHcS6'
        self.gt_channel.app_key = '7ic7HnWpuK7nYrdE94Cwt'
        self.gt_channel.master_secret = '6oaZcVm9fZ7aJbDh53Qoi5'

    def tearDown(self):
        pass
        # self.channel_fixture.cleanUp()

    def test_push_message_to_single(self):
        """
        测试推送到单个设备
        :return:
        """
        message = {
            "payload":"测试123"
        }

        result = self.gt_channel.push_message_to_single('3ff385f589e6a2ec71cb2ea84994bf17', message=message)

        self.assertEquals(result['result'], 'ok')


    def test_push_message_to_list(self):
        """
        测试推送到多个设备
        :return:
        """
        message = {
            "payload":"12222"
        }

        result = self.gt_channel.push_message_to_list(['3ff385f589e6a2ec71cb2ea84994bf17'], message=message)

        self.assertEquals(result['result'], 'ok')


class ALYipelineTestCase(BaseTestCase):
    """
    阿里云通道测试
    """


    def setUp(self):
        self.aly_channel = ALYChannel(self.ctx, 'fdb3509f076048a0af4a2d63eb2ee40d','ALYChannel', 'ALYChannel','',1)
        self.aly_channel.access_key_id = 'LTAIC6ZhbG7eZsNz'
        self.aly_channel.access_key_secret = 'g0t9C2lswSsQqMAAoK6CHDiCEGyboU'
        self.aly_channel.region_id = 'cn-hangzhou'
        self.aly_channel.app_key = '24835452'




    def tearDown(self):
        pass

    def test_push_message_to_single(self):
        """
        测试推送到单个设备
        :return:
        """

        message = {
            "payload": '测试'
        }
        result = self.aly_channel.push_message_to_single('8a6611b7c0514ad88de26b4095a7cc67', message=message)
        self.assertNotEquals(result['result'], 'ok')


    def test_push_message_to_list(self):
        """
        测试推送到多个设备
        :return:
        """
        message = {
            "payload":"aly测试123"
        }
        result = self.aly_channel.push_message_to_list(['8a6611b7c0514ad88de26b4095a7cc67'], message=message)
        self.assertNotEquals(result['result'], 'ok')