#!/usr/bin/python
# -*- encoding: utf-8 -*-

CONFIG = {
    'ENCODING': 'utf-8'
}

_app = None


def init_app(app):
    print 'init app in axf util'
    if not app:
        return

    if 'ENCODING' in app.config:
        CONFIG['ENCODING'] = app.config['ENCODING']

    global _app
    _app = app


def get_app():
    return _app