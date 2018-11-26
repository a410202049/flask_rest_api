#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti, get_jwt_identity, \
    jwt_refresh_token_required, get_raw_jwt, jwt_required, fresh_jwt_required

from server.exception import ERROR
from utils.db_session import DBSessionForWrite, DBSessionForRead

from server.base_resource import BaseResource, resource_method
from server.resource.v2 import v2
from server.models.UserModel import User
from utils.redis_cache import get_client


@v2.route('/auth/login')
class LoginResource(BaseResource):
    @resource_method()
    def post(self, **request):
        username = request.get('username')
        password = request.get('password')

        _redis = get_client()
        with DBSessionForRead() as session:
            user = session.query(User).filter(
                User.username == username
            ).scalar()
            is_pass = user.verify_password(password)

        if is_pass:
            user_ditc = {
                "username": user.username,
                "email": user.email
            }
            access_token = create_access_token(identity=user_ditc, fresh=True)
            refresh_token = create_refresh_token(identity=user_ditc)
            access_jti = get_jti(encoded_token=access_token)
            refresh_jti = get_jti(encoded_token=refresh_token)
            access_expires = current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES')
            refresh_expires = current_app.config.get('JWT_REFRESH_TOKEN_EXPIRES')
            _redis.set(access_jti, 'false', access_expires)
            _redis.set(refresh_jti, 'false', refresh_expires)
            ret = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            return self.make_response(ret)
        return self.make_response(resp_code=ERROR, resp_desc='用户或密码错误')


@v2.route('/auth/refresh')
class RefreshResource(BaseResource):
    @resource_method()
    @jwt_refresh_token_required
    def post(self, **request):
        _redis = get_client()
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        access_jti = get_jti(encoded_token=access_token)
        access_expires = current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES')
        _redis.set(access_jti, 'false', access_expires)
        ret = {'access_token': access_token}
        return self.make_response(ret)


@v2.route('/auth/access_revoke')
class AccessRevokeResource(BaseResource):
    @resource_method()
    @jwt_required
    def post(self, **request):
        _redis = get_client()
        jti = get_raw_jwt()['jti']
        access_expires = current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES')
        _redis.set(jti, 'true', access_expires)
        return self.make_response({"message": "Access token revoked"})


@v2.route('/auth/refresh_revoke')
class RefreshsRevokeResource(BaseResource):
    @resource_method()
    @jwt_refresh_token_required
    def post(self, **request):
        _redis = get_client()
        jti = get_raw_jwt()['jti']
        refresh_expires = current_app.config.get('JWT_REFRESH_TOKEN_EXPIRES')
        _redis.set(jti, 'true', refresh_expires)
        return self.make_response({"message": "Refresh token revoked"})


@v2.route('/protected')
class ProtectedResource(BaseResource):
    @fresh_jwt_required
    @resource_method()
    def post(self, **request):
        current_user = get_jwt_identity()
        return self.make_response({"current_user": current_user})
