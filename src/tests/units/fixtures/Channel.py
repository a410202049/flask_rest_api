#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import uuid

from library.db_session import DBSessionForWrite
from server.models.WalletModels import Channel, ChannelStatus, Application
from tests.units.fixtures import BaseFixture


class ChannelFixture(BaseFixture):
    """
    通道
    """
    pass



class GTChannelFixture(ChannelFixture):
    """
    个推通道
    """

    def __init__(self):
        self.channel = None

    def setUp(self):
        channel = Channel()
        channel.serial_no = uuid.uuid4().hex
        channel.name = 'GTChannel'
        channel.url = 'http://sdk.open.api.igexin.com/apiex.htm'
        channel.status = ChannelStatus.OK
        with DBSessionForWrite() as session:
            session.add(channel)
        self.channel = channel
        return self.channel

    def cleanUp(self):
        if self.channel:
            with DBSessionForWrite() as session:
                session.delete(self.channel)