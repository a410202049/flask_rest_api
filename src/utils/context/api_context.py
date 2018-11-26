#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import uuid
import time
from library.context.context import Context
from library.logger import log as logging


class ApiContext(Context):
    def __init__(self,
                 context=None,
                 request_id=None,
                 request_timestamp=None,
                 service_name=None,
                 service_version=None,
                 api_version=None,
                 ip=None,
                 method=None,
                 path=None):

        super(ApiContext, self).__init__(context)
        is_context_valid = context and isinstance(context, ApiContext)
        self.request_id = request_id or (context.request_id if is_context_valid else uuid.uuid4().hex)
        self.request_timestamp = request_timestamp or (context.request_timestamp if is_context_valid else time.time())
        self.service_name = service_name or (context.service_name if is_context_valid else None)
        self.service_version = service_version or (context.service_version if is_context_valid else None)
        self.api_version = api_version or (context.api_version if is_context_valid else None)
        self.log_type = context.tp if is_context_valid else 'NI'
        self.ip = ip or (context.ip if is_context_valid else None)
        self.method = method or (context.method if is_context_valid else None)
        self.path = path or (context.path if is_context_valid else None)

        self.server_name = context.server_name if hasattr(context, 'server_name') else None
        self.server_version = context.server_version if hasattr(context, 'server_version') else None
        self.hostname = context.hostname if hasattr(context, 'hostname') else None
        self.config_name = context.config_name if hasattr(context, 'config_name') else None

        self.logger = logging.get_logger(self, name='network')
