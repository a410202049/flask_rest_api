#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import uuid

from library.db_session import DBSessionForWrite
from server.models.WalletModels import Application
from tests.units.fixtures import BaseFixture


class ApplicationFixture(BaseFixture):
    """
    通道
    """
    pass



class GTApplicationFixture(ApplicationFixture):
    """
    个推通道
    """

    def __init__(self):
        self.channel = None

    def setUp(self,serial_no):
        app_id = Application()
        app_id.channel_no = serial_no
        app_id.app_no = '8CTEzxXUb78YbMfUHZHcS8v'
        app_id.key = 'APP_ID'
        app_id.value = '9CTEzxXUb78YbMfUHZHcS6v'
        app_id.display = u'应用ID'
        app_id.key_desc = u'安心付手机应用APP_ID【测试】'

        app_key = Application()
        app_key.channel_no = serial_no
        app_key.app_no = '8CTEzxXUb78YbMfUHZHcS8v'
        app_key.key = 'APP_KEY'
        app_key.value = '7ic7HnWpuK7nYrdE94Cwt'
        app_key.display = u'应用KEY'
        app_key.key_desc = u'安心付手机应用KEY【测试】'

        master_secret = Application()
        master_secret.channel_no = serial_no
        master_secret.app_no = '8CTEzxXUb78YbMfUHZHcS8v'
        master_secret.key = 'MASTER_SECRET'
        master_secret.value = '6oaZcVm9fZ7aJbDh53Qoi5'
        master_secret.display = u'应用密匙'
        master_secret.key_desc = u'安心付手机应用密匙【测试】'

        with DBSessionForWrite() as session:
            session.add(app_id)
            session.add(app_key)
            session.add(master_secret)
        self.app_id = app_id
        self.app_key = app_key
        self.master_secret = master_secret

    def cleanUp(self):
        if self.app_id:
            with DBSessionForWrite() as session:
                session.delete(self.app_id)
        if self.app_key:
            with DBSessionForWrite() as session:
                session.delete(self.app_key)
        if self.master_secret:
            with DBSessionForWrite() as session:
                session.delete(self.master_secret)