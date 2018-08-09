# -*- coding: utf-8 -*-
import logging


class RequireExceptionFilter(logging.Filter):
    """
    Useful for error-handling systems that attach to python logging.
    """

    def filter(self, record):
        return record.exc_info is not None
