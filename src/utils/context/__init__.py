#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import platform

CONFIG = {
    'SERVICE_NAME': '-',
    'SERVICE_VERSION': '-',
    'HOSTNAME': platform.node(),
    'CONFIG_NAME': '-'
}


def init_app(app):
    if not app:
        return

    print 'init context app'
    for key in CONFIG.keys():
        if key in app.config:
            print 'set %s = %s' % (key, app.config[key])
            CONFIG[key] = app.config[key]
