#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import functools
import json

from flask import request, current_app
from flask_restplus import Resource
from library.context.api_context import ApiContext
from library.logger import log as logging
from library.utils.dict_util import check_dict
from server.exception import SUCCESS, IllegalRequestException


class BaseResource(Resource):
    """
    基类
    """
    def __init__(self, api=None, *args, **kwargs):
        self.context = ApiContext(
            request_id=request.headers['REQUEST_ID'] if 'REQUEST_ID' in request.headers.keys() else None,
            request_timestamp=request.headers['X-TIMESTAMP'] if 'X-TIMESTAMP' in request.headers.keys() else None,
            service_name=current_app.config.get('SERVICE_NAME', None),
            service_version=current_app.config.get('SERVICE_VERSION', None),
            api_version=api.version if api else None,
            ip=request.remote_addr,
            method=request.method,
            path=request.path
        )
        self.context.config_name = current_app.config.get('CONFIG_NAME', None)
        self.context.config = current_app.config
        self.logger = logging.get_logger(context=self.context, name='network')
        self.logger.info('access {resource} request data is: [{request}]'
                         .format(resource=self.__class__.__name__,
                                 request=request.data or request.form.to_dict() or request.args.to_dict()))
        self.context.logger = self.logger
        super(BaseResource, self).__init__(api, *args, **kwargs)

    def make_response(self, response=None):
        base_resp = dict(resp_code=SUCCESS, resp_desc='成功')
        resp = dict(
            resp=base_resp,
        )

        if response:
            resp.update(response)
        self.logger.info('resp data is: [{resp}]'.format(resp=resp))
        return resp


def check_request(message_rules):

    def actual_decorator(func):

        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            # verify request data
            if message_rules:
                result, request = check_dict(request, message_rules)
                if not result:
                    raise IllegalRequestException(request)

            response = func(self, request, *args, **kwargs)

            response = response if response is not None else {}

            return response

        return wrapper

    return actual_decorator


def resource_method():
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            _args = tuple(kwargs.values())
            _args += args
            _kwargs = request.args.to_dict() if request.method == 'GET' else json.loads(request.get_data())

            return func(self, *_args, **_kwargs)

        return wrapper
    return actual_decorator
