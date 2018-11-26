#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import json
import time

from flask import Flask, jsonify
from flask import Response
from flask_restplus import Api
from utils import context
from utils.logger.log import init_logger_from_object

from flask_jwt_extended import JWTManager

app = None
jwt = None

def create_app(config):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    init_logger_from_object(config)

    global app
    app = Flask(__name__)

    api = Api(app=app, title=config.SERVICE_NAME, version=config.SERVICE_VERSION, doc=config.SWAGGER_PATH)

    app.config.from_object(config)

    # context init
    context.init_app(app)

    # v2.0.1 init
    from server.resource.v2 import init_api
    init_api(api)

    # exception handler
    from server.exception import init_api_error
    init_api_error(api)

    # init utils
    import utils
    utils.init_app(app)

    # init db
    from utils import db_session
    db_session.init_app(app)

    # init redis
    from utils import redis_cache
    redis_cache.init_app(app)

    from server.dao import init_app
    init_app(app)

    global jwt
    jwt = JWTManager(app)

    from utils.redis_cache import get_client

    # issues flask-jwt-extended 和 flask_restplaus 不能调用  jwt.expired_token_loader 等回调
    # 参考https://github.com/vimalloc/flask-jwt-extended/issues/86

    # @jwt.user_claims_loader
    # def add_claims_to_access_token(identity):
    #     # 再token中添加额外数据
    #     return {
    #         'email': identity['email']
    #     }

    # @jwt.user_identity_loader
    # def user_identity_lookup(user):
    #     return user

    # @jwt.user_loader_callback_loader
    # def user_loader_callback(identity):
    #
    #     current = {
    #         "test": "123",
    #         "user": identity
    #     }
    #     return current

    @jwt.token_in_blacklist_loader
    def check_if_token_is_revoked(decrypted_token):
        # 检查token是否被作废
        _redis = get_client()
        jti = decrypted_token['jti']
        entry = _redis.get(jti)
        if entry is None:
            return True
        return entry == 'true'


    return app




class ResourceResponse(Response):
    """
    response
    """
    def __init__(self, resp_code, resp_desc, timestamp=None, response=None, **kwargs):
        self.resp_code = resp_code
        self.resp_desc = resp_desc
        self.timestamp = timestamp if timestamp else str(time.time()).replace('.', '')

        if response is None:
            kwargs['response'] = json.dumps(self.get_base_response())
        super(ResourceResponse, self).__init__(**kwargs)
        self.headers = self.get_response_headers()

    def get_response_headers(self):
        """
        获取响应头
        :return:
        """
        headers = {'content-type': 'application/json;charset=utf-8',
                   'X-timestamp': self.timestamp
                   }
        return headers

    def get_base_response(self):
        base_resp = dict(
            resp_code=self.resp_code,
            resp_desc=self.resp_desc,
        )

        return dict(resp=base_resp)
