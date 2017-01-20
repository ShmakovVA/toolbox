# -*- coding: utf-8 -*-
import logging
from datetime import datetime, date, timedelta
from time import mktime
from collections import namedtuple

import pytz
from furl import furl, omdict1D

log = logging.getLogger(__name__)

EPOCH = datetime(1970, 1, 1, tzinfo=pytz.utc)


def compare_urls(url, other_url):
    """
    Compare two URLs. This function doesn't care about the order of querystring
    parameters.

    :param url: url string or furl object
    :param other_url: url string or furl object
    :return: bool of whether we consider them the same
    """
    def sort_qs_params(url):
        url.args = omdict1D(sorted(url.args.allitems()))
    u1 = furl(url)
    sort_qs_params(u1)
    u2 = furl(other_url)
    sort_qs_params(u2)
    return u1 == u2


def date_range(start_date, stop_date=None):
    """
    Yields date objects between `start_date` and `stop_date` (inclusive).
    `stop_date` can also be an integer offset of days or a timedelta.

    :param start_date: first date
    :param stop_date: last date (default: today) or offset (int or timedelta)
    """
    if isinstance(stop_date, int):
        stop_date = start_date + timedelta(days=stop_date)
    elif isinstance(stop_date, timedelta):
        stop_date = start_date + stop_date
    else:
        stop_date = stop_date or date.today()
    current = start_date
    while current <= stop_date:
        yield current
        current += timedelta(days=1)


def datetime_to_epoch(date_time):
    # type: (datetime.datetime) -> int
    u""" Convert a datetime object to epoch seconds. """

    if date_time.tzinfo:
        # incompatible with naive datetimes
        return int((date_time - EPOCH).total_seconds())

    else:
        return int(mktime(date_time.timetuple()))


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


def s_to_hms(seconds, d=60*60, r=[]):
    """
    Split seconds into more human-readable hours, minutes and seconds.

    :param seconds: integer seconds
    :return: namedtuple of ['hours', 'minutes', 'seconds']
    """
    if seconds == 0:
        return namedtuple('hms', ['hours', 'minutes', 'seconds'])(*r)
    return s_to_hms(seconds % d, d // 60, r + [seconds // d])


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

