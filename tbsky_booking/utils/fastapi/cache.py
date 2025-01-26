from typing import Awaitable, Callable, Optional, ParamSpec, Type, TypeVar

from fastapi_cache import Coder, KeyBuilder
from fastapi_cache.decorator import cache
from starlette.requests import Request
from starlette.responses import Response

from .coder import ORJsonCoder

__all__ = ["cache_result", "fast_cache_result"]

P = ParamSpec("P")
R = TypeVar("R")


def request_key_builder(
    func,
    namespace: str = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs,
):

    result = ":".join(
        [
            namespace,
            request.method.lower(),
            request.url.path,
            repr(sorted(request.query_params.items())),
        ]
    )
    return result


def cache_result(
    expire: Optional[int] = 120,
    coder: Optional[Type[Coder]] = ORJsonCoder,
    key_builder: Optional[KeyBuilder] = request_key_builder,
    namespace: str = "",
    injected_dependency_namespace: str = "__fastapi_cache",
):
    return cache(
        expire=expire,
        coder=coder,
        key_builder=key_builder,
        namespace=namespace,
        injected_dependency_namespace=injected_dependency_namespace,
    )


def fast_cache_result(func: Callable[P, Awaitable[R]]):
    return cache_result()(func)
