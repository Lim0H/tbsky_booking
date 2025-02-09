from tbsky_booking.utils.itertools import first_or_none, first_or_value


def test_first_or_value():
    assert first_or_value([1, 2, 3], 0) == 1
    assert first_or_value([], 0) == 0


def test_first_or_none():
    assert first_or_none([1, 2, 3]) == 1
    assert first_or_none([]) is None


def test_first_or_value_with_custom_type():
    class CustomType:
        def __init__(self, value):
            self.value = value

    custom_list = [CustomType(1), CustomType(2), CustomType(3)]
    assert first_or_value(custom_list, CustomType(0)).value == 1
    assert first_or_value([], CustomType(0)).value == 0


def test_first_or_none_with_custom_type():
    class CustomType:
        def __init__(self, value):
            self.value = value

    custom_list = [CustomType(1), CustomType(2), CustomType(3)]
    assert first_or_none(custom_list).value == 1
    assert first_or_none([]) is None
