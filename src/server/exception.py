#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from library.logger import log as logging
from server.app import ResourceResponse

SUCCESS = 'RES0000'
INVALID_REQUEST_VALUE = 'RES0001'
SIGNATURE_ERROR = 'RES0002'
RULE_NOT_FOUND = 'RES0003'
SYSTEM_ERROR = 'RES9999'


logger = logging.get_logger()


def init_api_error(api):
    if not api:
        raise RuntimeError('api is None')

    @api.errorhandler
    def exception_error_handler(e):
        logger.exception(u'service has exception')

        error_code, error_msg = SYSTEM_ERROR, 'system error'
        if isinstance(e, ResourceBaseException):
            error_code = e.error_code
            error_msg = e.error_msg
        elif isinstance(e, Exception):
            logger.exception(u'service has exception: {0}'.format(e.message))

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
