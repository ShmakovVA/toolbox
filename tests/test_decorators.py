# -*- coding: utf-8 -*-
import json
import logging
from time import sleep

from toolbox.decorators import suppress_logging, time_call

from . import TestCase, MagicMock


class TestSuppressLogging(TestCase):
    def test_suppress_logging(self):
        base_disable = logging.root.manager.disable
        self.assertEqual(base_disable, logging.NOTSET)

        with suppress_logging(logging.INFO):
            self.assertEqual(logging.root.manager.disable, logging.INFO)
        self.assertEqual(logging.root.manager.disable, logging.NOTSET)

        @suppress_logging(logging.INFO)
        def suppressed_func():
            self.assertEqual(logging.root.manager.disable, logging.INFO)

        suppressed_func()
        self.assertEqual(logging.root.manager.disable, logging.NOTSET)


class TestTimeCall(TestCase):
    def test_timed_call(self):
        mock_logger = MagicMock()

        @time_call(mock_logger, 'test_func')
        def timed_func():
            sleep(1)

        timed_func()
        self.assertTrue(mock_logger.info.called)

        args, _ = mock_logger.info.call_args
        result = json.loads(args[0])

        self.assertEqual(result['type'], 'test_func')
        self.assertGreaterEqual(result['duration'], 1.0)
