#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

from config import get_config
from server.app import create_app
from library.context.context import Context

class BaseTestCase(unittest.TestCase):
    """
    base test case
    """
    def __init__(self, methodName='runTest'):
        self.ctx = Context()
        super(BaseTestCase, self).__init__(methodName)

    def setUp(self):
        app = create_app(get_config('unit_test'))
        app.app_context().push()

