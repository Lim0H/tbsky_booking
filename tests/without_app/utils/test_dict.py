# test_dict.py
import pytest

from tbsky_booking.utils.dict import get_value_from_dict


def test_get_value_from_dict():
    data = {"key": "value"}
    key = "key"
    default_value = "default"
    assert get_value_from_dict(data, key, default_value) == "value"


def test_get_value_from_dict_with_default():
    data = {}
    key = "key"
    default_value = "default"
    assert get_value_from_dict(data, key, default_value) == "default"


def test_get_value_from_dict_with_nested_key():
    data = {"key": {"nested_key": "value"}}
    key = "key.nested_key"
    default_value = "default"
    assert get_value_from_dict(data, key, default_value) == "value"


def test_get_value_from_dict_with_nested_key_and_default():
    data = {"key": {}}
    key = "key.nested_key"
    default_value = "default"
    assert get_value_from_dict(data, key, default_value) == "default"


def test_get_value_from_dict_with_invalid_key():
    data = {"key": "value"}
    key = "invalid_key"
    default_value = "default"
    assert get_value_from_dict(data, key, default_value) == "default"


def test_get_value_from_dict_with_none_data():
    data = {}
    key = "key"
    default_value = "default"
    assert get_value_from_dict(data, key, default_value) == "default"


def test_get_value_from_dict_with_none_default_value():
    data = {"key": "value"}
    key = "key"
    default_value = None
    assert get_value_from_dict(data, key, default_value) == "value"
