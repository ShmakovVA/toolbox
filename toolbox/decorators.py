# -*- coding: utf-8 -*-
import json
import logging
import time
from functools import wraps

from django.core.cache import caches

from toolbox.exceptions import LockFailure

log = logging.getLogger(__name__)


class Lock(object):
    """
    Context manager / decorator that tries to aquire a lock before proceding,
    raises LockFailure if another process is already holding that lock.

    :param key: locker key (prefixed with `prefix`)
    :param timeout: timeout in seconds (default None)
    :param prefix: optional prefix (default 'sem_')
    :param locker_name: name of cache (default 'locker')
    """
    LockFailure = LockFailure

    def __init__(self, key, timeout=None, prefix='sem_', locker_name='locker'):
        self.key = prefix + key
        self.timeout = timeout
        self.locker = caches[locker_name]

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapper

    def __enter__(self):
        if not self.locker.add(self.key, True, self.timeout):
            raise self.LockFailure(
                'Failed to aquire lock "{}"'.format(self.key))

    def __exit__(self, *exc):
        self.locker.delete(self.key)
lock = Lock


class SuppressLogging(object):
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
suppress_logging = SuppressLogging


def time_call(logger, call_type, context_func=None):
    """
    Log duration of decorated function in JSON format.

    `context_func`, if passed, will be called with the decorated function's
    *args and **kwargs and is expected to return a dict that will be included in
    the log entry.

    e.g.:

    def f(*args, **kwargs):
        return {'slug': kwargs['slug']}

    @time_call(my_logger, 'mymodule.my_func', f)
    def my_func(var1, slug='myslug'):
        do_something()

    ==>

    my_logger.info(json.dumps({
            'type': 'mymodule.my_func',
            'slug': 'myslug',
            'duration': <call duration in float-seconds>,
    }))

    :param logger: logger to log to
    :param call_type: `type` key in log, should say what was timed
    :param context_func: callable that returns a dict
    """
    def decorate(func):
        @wraps(func)
        def call(*args, **kwargs):
            start_time = time.time()
            context = {}
            if context_func:
                context.update(context_func(*args, **kwargs))
            try:
                result = func(*args, **kwargs)
            except:
                raise
            finally:
                end_time = time.time()
                duration = end_time - start_time
                try:
                    context.update({
                        'type': call_type,
                        'duration': duration,
                    })
                    logger.info(json.dumps(context))
                except:
                    log.exception('time_call() failed to log')
            return result
        return call
    return decorate

