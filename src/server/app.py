#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import json
import time

from flask import Flask
from flask import Response
from flask_restplus import Api
from library import context
from library.logger.log import init_logger_from_object

app = None


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

    # init db
    from library import db_session
    db_session.init_app(app)

    from server.dao import init_app
    init_app(app)

    return app


class ResourceResponse(Response):
    """
    response
    """
    def __init__(self, resp_code, resp_desc, timestamp=None, response=None, **kwargs):
        self.resp_code = resp_code
        self.resp_desc = resp_desc
        self.timestamp = timestamp if timestamp else str(time.time()).replace('.', '')

        self.signature = '123'
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
                   'X-timestamp': self.timestamp,
                   'X-sign': self.signature}
        return headers

    def get_base_response(self):
        base_resp = dict(
            resp_code=self.resp_code,
            resp_desc=self.resp_desc,
        )

        return dict(resp=base_resp)
