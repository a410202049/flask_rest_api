#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from context import Context
from ..db_session import DBSessionForRead, DBSessionForWrite


class AppContext(Context):
    def __init__(self,
                 context=None,
                 name=None,
                 version=None,
                 service=None,
                 method=None,
                 req_ip=None,
                 base_path=None,
                 path=None,
                 req_host=None
                 ):

        super(AppContext, self).__init__(context)

        is_context_valid = context and isinstance(context, AppContext)
        self.name = name or (context.name if is_context_valid else None)
        self.version = version or (context.version if is_context_valid else None)
        self.service = service or (context.service if is_context_valid else None)
        self.method = method or (context.method if is_context_valid else None)
        self.req_ip = req_ip or (context.req_ip if is_context_valid else None)
        self.base_path = base_path or (context.base_path if is_context_valid else None)
        self.path = path or (context.path if is_context_valid else None)
        self.req_host = req_host or (context.req_host if is_context_valid else None)

        from ..structed_log.app_log import AppLog
        self.log = AppLog(self)

    def open_readable_db_sesion(self):
        return DBSessionForRead()

    def open_writable_db_sesion(self):
        return DBSessionForWrite()


