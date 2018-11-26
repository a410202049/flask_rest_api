#!/usr/bin/python
# -*- encoding: utf-8 -*-
import traceback

from library.context.context import Context
ctx = Context()


def async(f):
    import gevent
    from gevent import Greenlet

    def wrapper(*args, **kwargs):
        t = Greenlet.spawn(f, *args, **kwargs)
        gevent.joinall([t])
    return wrapper


def _send_email(mail, msg):
    try:

        from . import get_app
        with get_app().app_context():
            mail.send(msg)
    except Exception, e:
        # ignore
        ctx.logger.exception(e.message)
        pass


@async
def _send_async_email(mail, msg):
    _send_email(mail, msg)


def send_warning_email(title, body, recipients):

    try:
        from flask_mail import Message
        from flask_mail import Mail
        from flask import current_app

        msg = Message(title, sender=current_app.config['MAIL_USERNAME'], recipients=recipients)
        msg.body = body

        mail = Mail()
        mail.init_app(current_app)

        _send_async_email(mail, msg)
    except Exception, ex:
        # ignore
        ctx.logger.exception(ex.message)
        pass


def get_exception_message(ex):
    if not ex:
        return 'no error object found'

    msg = traceback.format_exception_only(type(ex), ex)
    if msg:
        msg = msg[0].strip()
        if len(msg) > 100:
            msg = msg[:92] + '...'

        return msg

    return '-'