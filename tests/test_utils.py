# -*- coding: utf-8 -*-
import pytz
from datetime import datetime, date

from toolbox.utils import (
    date_range,
    datetime_to_epoch,
    s_to_hms,
    compare_urls,
    process_with_threadpool,
    list_chunker,
    # queryset_chunker,
    set_chunker
)

from . import TestCase


class TestTimeUtils(TestCase):
    def test_date_range(self):
        start_date = date(2018, 1, 1)

        relative_range = list(date_range(start_date, 2))
        self.assertListEqual(
            relative_range,
            [date(2018, 1, 1), date(2018, 1, 2), date(2018, 1, 3)]
        )

        absolute_range = list(date_range(start_date, date(2018, 1, 2)))
        self.assertListEqual(
            absolute_range,
            [date(2018, 1, 1), date(2018, 1, 2)]
        )

        dynamic_range = list(date_range(start_date))
        self.assertEqual(dynamic_range[0], start_date)
        self.assertEqual(dynamic_range[-1], date.today())

    def test_datetime_to_epoch(self):
        self.assertEqual(
            datetime_to_epoch(datetime(2018, 1, 1, 1, 1)),
            1514764860
        )

        self.assertEqual(
            datetime_to_epoch(datetime(2018, 1, 1, 1, 1, tzinfo=pytz.UTC)),
            1514768460
        )

    def test_s_to_hms(self):
        self.assertEqual(tuple(s_to_hms(0)), (0, 0, 0))
        self.assertEqual(tuple(s_to_hms(61)), (0, 1, 1))
        self.assertEqual(tuple(s_to_hms(3661)), (1, 1, 1))


class TestUtils(TestCase):
    def test_compare_urls(self):
        self.assertTrue(compare_urls(
            'http://some.host/some/path',
            'http://some.host/some/path'))
        self.assertFalse(compare_urls(
            'http://some.host/some/path',
            'http://some.host/some/other/path'))

        self.assertTrue(compare_urls(
            'http://some.host/some/path?a=1&a=2&b=2',
            'http://some.host/some/path?a=1&a=2&b=2'))
        self.assertTrue(compare_urls(
            'http://some.host/some/path?b=2&a=1&a=2',
            'http://some.host/some/path?a=1&a=2&b=2'))
        self.assertFalse(compare_urls(
            'http://some.host/some/path?a=1&b=3',
            'http://some.host/some/path?a=1&b=2'))
        self.assertFalse(compare_urls(
            'http://some.host/some/path?b=3&a=1',
            'http://some.host/some/path?a=1&b=2'))

    def test_process_with_threadpool(self):
        result = process_with_threadpool([1, 2, 3, 4], lambda x: x ** 2)
        result_list = sorted([f.result() for f in result.keys()])
        self.assertListEqual(result_list, [1, 4, 9, 16])


class TestChunkers(TestCase):
    def test_list_chunker(self):
        sample_list = range(10)
        self.assertListEqual(
            list(list_chunker(sample_list, chunk_size=3)),
            [
                [0, 1, 2],
                [3, 4, 5],
                [6, 7, 8],
                [9, ]
            ]
        )

    def test_set_chunker(self):
        sample_list = range(10)
        self.assertListEqual(
            list(set_chunker(sample_list, chunk_size=3)),
            [
                {0, 1, 2},
                {3, 4, 5},
                {6, 7, 8},
                {9, }
            ]
        )

    def test_queryset_chunker(self):
        pass
