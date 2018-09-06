#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from task import celery
from library.context.context import Context

ctx = Context()

if __name__ == '__main__':
    # handle_income_info()
    pass


@celery.task()
def sync_income_info():
    pass
    # handle_income_info()
