# -*- coding: utf-8 -*-
import json
import time
from functools import wraps


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
                    pass
            return result
        return call
    return decorate

