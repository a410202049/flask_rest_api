#!/usr/bin/python
# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

from sqlalchemy import desc

from server.dao import BaseDao
from server.models.UserModel import User


class UserDao(BaseDao):
    """
    用户操作dao
    """

    def get_users(self):

        users = self.get_sql_session().query(User).all()

        return users
