# test_datetime.py
from datetime import datetime

import pytest

from tbsky_booking.utils.datetime import format_datetime, parse_time


def test_format_datetime():
    dt = datetime(2022, 1, 1, 12, 0, 0)
    assert format_datetime(dt) == "2022-01-01T12:00:00Z"


def test_parse_time():
    time_str = "12:00"
    assert parse_time(time_str) == 720


def test_parse_time_with_empty_string():
    assert parse_time("") is None
