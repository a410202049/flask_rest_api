#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import uuid

from library.db_session import DBSessionForWrite
from server.models.WalletModels import Policy, PolicyStatus
from tests.units.fixtures import BaseFixture


class PolicyFixture(BaseFixture):
    """
    policy
    """

    def __init__(self):
        self.policy = []

    def setUp(self):
        filter_policy = Policy()
        filter_policy.serial_no = uuid.uuid4().hex
        filter_policy.name = 'DemoFilter'
        filter_policy.rule = 'FILTER::TestRule::DemoFilter'
        filter_policy.status = PolicyStatus.OK

        weight_policy = Policy()
        weight_policy.serial_no = uuid.uuid4().hex
        weight_policy.name = 'DemoWeight'
        weight_policy.rule = 'WEIGHT::TestRule::DemoWeight'
        weight_policy.status = PolicyStatus.OK

        with DBSessionForWrite() as session:
            session.add(filter_policy)
            session.add(weight_policy)
        self.policy.append(filter_policy)
        self.policy.append(weight_policy)

        return self.policy

    def cleanUp(self):
        for policy in self.policy:
            with DBSessionForWrite() as session:
                session.delete(policy)
