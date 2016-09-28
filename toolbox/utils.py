# -*- coding: utf-8 -*-
import logging
import time
from functools import wraps

log = logging.getLogger(__name__)


def set_chunker(iterable, chunk_size=100):
    """
    Generator function that yields `chunk_size`-sized sets from an iterable.

    :param iterable: an iterable to cut up
    :param chunk_size: chunk size, default 100
    """
    s = set()
    for i, id in enumerate(iterable, start=1):
        s.add(id)
        if not i % chunk_size:
            chunk = s
            s = set()
            yield chunk
    if s:
        yield s


def list_chunker(iterable, chunk_size=100):
    """
    Generator function that yields `chunk_size`-sized lists from an iterable.

    :param iterable: an iterable to cut up
    :param chunk_size: chunk size, default 100
    """
    l = []
    for i, id in enumerate(iterable, start=1):
        l.append(id)
        if not i % chunk_size:
            chunk = l
            l = []
            yield chunk
    if l:
        yield l


def queryset_chunker(qs, chunk_size=100):
    """
    Generator function that yields `chunk_size`-sized slices of QuerySet-like
    objects. For example QuerySet:s and SportamoreSearchQuerySet:s.

    :param qs: QuerySet-like to slice
    :param chunk_size: chunk size, default 100
    """
    idx = 0
    chunk = qs[idx:idx+chunk_size]
    while chunk:
        yield chunk
        idx += chunk_size
        chunk = qs[idx:idx+chunk_size]


class suppress_logging(object):
    """
    A contextmanager/decorator that will prevent any logging messages
    triggered during the body from being processed.

    :param target_level: Anything at or below this level will be suppressed.
    """

    def __init__(self, target_level=logging.CRITICAL):
        self.target_level = target_level

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper

    def __enter__(self):
        self.previous_level = logging.root.manager.disable
        logging.disable(self.target_level)

    def __exit__(self, *exc):
        logging.disable(self.previous_level)


def datetime_to_epoch(date_time):
    # type: (datetime) -> int
    u""" Convert a datetime object to an epoch timestamp. """
    return int(time.mktime(date_time.timetuple()))

