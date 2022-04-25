import datetime

from analyzer.utils import format_date_str, format_date, merge_dicts


def test_format_date_str():
    assert format_date(None) == datetime.datetime(1, 1, 1)
    assert format_date("2022-10-05T21:14:17Z") == datetime.datetime(2022, 10, 5, 21, 14, 17)
