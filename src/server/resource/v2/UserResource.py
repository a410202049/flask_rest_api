#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from server.base_resource import BaseResource, resource_method, check_request
from server.dao.user_dao import UserDao
from server.resource.v2 import v2
from utils.dict_util import StrRule


@v2.route('/users')
class UserResource(BaseResource):
    """用户列表"""

    @resource_method()
    def get(self):
        # _redis = get_client()

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
    @check_request({
        'name': StrRule('.+', nullable=False, illegal_value_notice='名称不能为空'),
        'password': StrRule('^[\@A-Za-z0-9\!\#\$\%\^\&\*\.\~]{6,32}$', nullable=False,
                            illegal_value_notice=u'密码由6-32位字符或者数字组成'),
    })
    def post(self, user_id, **request):
        print request
        return self.make_response({'user_id': user_id})
