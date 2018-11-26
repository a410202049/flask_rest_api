#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from flask_jwt_extended.exceptions import RevokedTokenError, FreshTokenRequired, InvalidHeaderError
from jwt import ExpiredSignatureError
from utils.logger import log as logging
from server.app import ResourceResponse

SUCCESS = 'RES0000'
ERROR = 'RES0001'
INVALID_REQUEST_VALUE = 'RES0002'
SIGNATURE_ERROR = 'RES0003'
RULE_NOT_FOUND = 'RES0004'
TOKEN_EXPIRED = 'RES0005'
TOKEN_REVOKED = 'RES0006'
TOKEN_FRESH = 'RES0007'
INVALID_HEADER = 'RES0008'

SYSTEM_ERROR = 'RES9999'
logger = logging.get_logger()


def init_api_error(api):
    if not api:
        raise RuntimeError('api is None')

    @api.errorhandler(ExpiredSignatureError)
    def handle_expired_error(e):
        logger.exception(u'ExpiredSignatureError {0}'.format(e.message))
        error_code, error_msg = TOKEN_EXPIRED, 'Token过期'
        resp = ResourceResponse(error_code, error_msg)
        return resp.get_base_response(), 401, resp.get_response_headers()

    @api.errorhandler(RevokedTokenError)
    def handle_revoked_token_error(e):
        logger.exception(u'RevokedTokenError {0}'.format(e.message))
        error_code, error_msg = TOKEN_REVOKED, 'Token已作废'
        resp = ResourceResponse(error_code, error_msg)
        return resp.get_base_response(), 401, resp.get_response_headers()

    @api.errorhandler(InvalidHeaderError)
    def handle_revoked_token_error(e):
        logger.exception(u'InvalidHeaderError {0}'.format(e.message))
        error_code, error_msg = INVALID_HEADER, '无效的header请求'
        resp = ResourceResponse(error_code, error_msg)
        return resp.get_base_response(), 401, resp.get_response_headers()

    # InvalidHeaderError

    @api.errorhandler(FreshTokenRequired)
    def handle_revoked_token_error(e):
        logger.exception(u'RevokedTokenError {0}'.format(e.message))
        error_code, error_msg = TOKEN_FRESH, '请使用新鲜的Token'
        resp = ResourceResponse(error_code, error_msg)
        return resp.get_base_response(), 401, resp.get_response_headers()

    @api.errorhandler
    def exception_error_handler(e):
        logger.exception(u'service has exception')
        error_code, error_msg = SYSTEM_ERROR, 'system error'
        if isinstance(e, ResourceBaseException):
            error_code = e.error_code
            error_msg = e.error_msg
        elif isinstance(e, Exception):
            logger.exception(u'service has exception: {0}'.format(e.message))
            import traceback
            from flask import current_app
            from utils import email_util

            title = u'ApiServer-%s-%s' % (current_app.config['CONFIG_NAME'], email_util.get_exception_message(e))
            body = u'ApiServer异常: \n{message}'.format(message=traceback.format_exc())
            email_util.send_warning_email(title, body, ['gaoyuan@axinfu.com'])

        resp = ResourceResponse(error_code, error_msg)
        return resp.get_base_response(), 200, resp.get_response_headers()


class ResourceBaseException(Exception):
    def __init__(self, error_msg, error_code, error_data=None):
        if not isinstance(error_code, (int, basestring)) and not isinstance(error_msg, basestring):
            raise RuntimeError(
                u'error_code is required as (int, basestring) and error_msg is required as basestring, but got(%s, %s)'
                % (type(error_code), type(error_msg)))

        super(ResourceBaseException, self).__init__(error_msg)

        self.error_code = error_code
        self.error_msg = error_msg
        self.error_data = error_data
        self.message = (error_code, error_msg)


class BusinessException(ResourceBaseException):
    def __init__(self, error_msg, error_code, resp_dict=None):
        super(BusinessException, self).__init__(error_msg, error_code, resp_dict)


class SystemException(ResourceBaseException):
    def __init__(self, error_msg, resp_code=SYSTEM_ERROR, resp_dict=None):
        super(SystemException, self).__init__(error_msg, resp_code, resp_dict)


class IllegalRequestException(ResourceBaseException):
    def __init__(self, error_msg, resp_code=INVALID_REQUEST_VALUE, resp_dict=None):
        super(IllegalRequestException, self).__init__(error_msg, resp_code, resp_dict)


class AccessException(BusinessException):
    def __init__(self, error_msg, error_code, resp_dict=None):
        super(AccessException, self).__init__(error_msg, error_code, resp_dict)


class ServiceNotFoundException(Exception):
    def __init__(self, api_version, service):
        super(ServiceNotFoundException, self).__init__('service [%s] not found in api [%s]' % (service, api_version))

        self.api_version = api_version
        self.service = service


class SignErrorException(ResourceBaseException):
    def __init__(self, error_msg, error_code=SIGNATURE_ERROR, resp_dict=None):
        super(SignErrorException, self).__init__(error_msg, error_code, resp_dict)


class MethodNotFoundException(Exception):
    def __init__(self, api_version, service, method):
        super(MethodNotFoundException, self).__init__(
            'method [%s] of service [%s] not found in api [%s]' % (method, service, api_version))

        self.api_version = api_version
        self.service = service
        self.method = method
