import asyncio
from functools import wraps
from typing import Any, Callable, Coroutine, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")

__all__ = ["to_async"]


def to_async(func: Callable[P, T]) -> Callable[P, Coroutine[Any, Any, T]]:
    """
    Dekorator, który przekształca funkcję synchroniczną w asynchroniczną.

    Args:
        func (Callable[P, T]): Funkcja synchroniczna.

    Returns:
        Callable[P, Coroutine[T]]: Funkcja asynchroniczna.
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Coroutine[Any, Any, T]:
        return asyncio.to_thread(func, *args, **kwargs)

    return wrapper
