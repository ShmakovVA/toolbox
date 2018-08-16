# -*- coding: utf-8 -*-
import logging
from toolbox.log import RequireExceptionFilter

from . import TestCase, MagicMock

class TestRequireExceptionFilter(TestCase):
    def setUp(self):
        self.logger = logging.Logger('test_log')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addFilter(RequireExceptionFilter())
        self.handler = MagicMock(level=logging.DEBUG)
        self.logger.addHandler(self.handler)

    def test_plain_message(self):
        self.logger.info('some message')
        self.assertEqual(self.handler.handle.call_count, 0)

    def test_message_with_exception(self):
        self.logger.exception('some message')
        self.assertEqual(self.handler.handle.call_count, 1)
