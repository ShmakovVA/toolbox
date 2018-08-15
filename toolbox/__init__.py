# -*- coding: utf-8 -*-
from . import _vcs
from .utils import (
    compare_urls,
    date_range,
    datetime_to_epoch,
    list_chunker,
    queryset_chunker,
    s_to_hms,
    set_chunker,
    process_with_threadpool
)

__all__ = [
    'compare_urls',
    'date_range',
    'datetime_to_epoch',
    'list_chunker',
    'queryset_chunker',
    's_to_hms',
    'set_chunker',
    'process_with_threadpool'
]

__version__ = _vcs.__version__.split('.')
