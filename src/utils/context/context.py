#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import uuid
from . import CONFIG
from ..logger import log as logging


class Context(object):
    def __init__(self, context=None):
        # self.log = None
        if context:
            self.request_id = context.request_id
            self.server_version = context.server_version
            self.server_name = context.server_name
            self.hostname = context.hostname
            self.config_name = context.config_name
            self.logger = logging.get_logger(self)
        else:
            self.request_id = uuid.uuid1().hex
            self.server_name = CONFIG['SERVICE_NAME']
            self.server_version = CONFIG['SERVICE_VERSION']
            self.hostname = CONFIG['HOSTNAME']
            self.config_name = CONFIG['CONFIG_NAME']
            self.logger = logging.get_logger(self)

    def get_service_status(self):
        return \
            '%s<br>' \
            'I\'m still alive.<br>' \
            '%s @ %s - %s using %s<br>' \
            'v%s' \
            % (self.serial, self.service_id, self.server_id, self.hostname, self.config_name, self.version)


class SystemContext(Context):

    def __init__(self):
        super(SystemContext, self).__init__()
        self.serial = 'system'
