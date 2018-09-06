#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from server.resource.v2.channel.base import ChannelManager
from tests.units import BaseTestCase
from tests.units.fixtures.Channel import ChannelFixture
from tests.units.fixtures.Policy import PolicyFixture


class SetPolicyTestCase(BaseTestCase):
    """
    test channel manager
    """
    def setUp(self):
        super(SetPolicyTestCase, self).setUp()
        self.channel_fixture = ChannelFixture()
        self.channel = self.channel_fixture.setUp()

        self.policy_fixture = PolicyFixture()
        self.policy = self.policy_fixture.setUp()

    def tearDown(self):
        self.channel_fixture.cleanUp()
        self.policy_fixture.cleanUp()

    def test_set_policy_by_default(self):
        """
        set policy
        :return:
        """
        channel_manager = ChannelManager()

        for _filter in channel_manager.filters:
            self.assertEquals(_filter.__name__, 'DemoFilter')

    def test_get_filtered_channel(self):
        channel_manager = ChannelManager()
        channel_manager.get_filtered_channel(channels=[self.channel])

    def test_get_weighted_channel(self):
        channel_manager = ChannelManager()
        channel_manager.get_weighted_channel(channels=[self.channel, self.channel])

    def test_get_channel(self):
        channel_manager = ChannelManager()
        channel_manager.get_channel()

