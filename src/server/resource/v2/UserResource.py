#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from server.base_resource import BaseResource, resource_method
from server.dao.user_dao import UserDao
from server.resource.v2 import v2


@v2.route('/users')
class UserResource(BaseResource):
    """用户列表"""

    @resource_method()
    def get(self):
        with UserDao(self.context) as user_dao:
            users = user_dao.get_users()

        name_list = []
        for user in users:
            name_list.append(user.username)

        return self.make_response({'name_list': name_list})


@v2.route('/users/<string:user_id>')
class UserResource(BaseResource):
    """用户列表"""

    @resource_method()
    def get(self, user_id, **request):
        print request
        return self.make_response({'user_id': user_id})
