__all__ = ["first_or_value", "first_or_none"]


from typing import Optional


def first_or_value[T](list_of_values: list[T], value: T) -> T:
    if list_of_values:
        return list_of_values[0]
    return value


def first_or_none[T](list_of_values: list[T]) -> Optional[T]:
    if list_of_values:
        return list_of_values[0]
    return None
