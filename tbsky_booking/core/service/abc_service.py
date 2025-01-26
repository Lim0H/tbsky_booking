from abc import ABC
from typing import Generator, Iterable, Optional

__all__ = [
    "GetService",
    "AddService",
    "EditService",
    "DeleteService",
    "GenericService",
    "EmptyService",
    "FunctorGetService",
]


class EmptyService[T](ABC):
    def __init__(self, *args, **kwargs):
        self.__post_init__(*args, **kwargs)

    def __post_init__(self, *args, **kwargs):
        pass


class GetService[T](EmptyService, ABC):
    async def get(self, *args, **kwargs) -> list[T]:
        raise NotImplementedError

    async def get_iter(self, *args, **kwargs) -> Generator[T, None, None]:
        raise NotImplementedError

    async def get_first(self, *args, **kwargs) -> Optional[T]:
        result = await self.get(*args, **kwargs)
        return result[0] if result else None

    async def get_one(self, *args, **kwargs) -> T:
        result = await self.get(*args, **kwargs)
        if result:
            return result[0]
        raise ValueError


class FunctorGetService[T](GetService, ABC):
    async def __call__(self, *args, **kwargs) -> list[T]:
        return await self.get(*args, **kwargs)


class AddService[T](EmptyService, ABC):
    async def add(self, model: T) -> T:
        raise NotImplementedError

    async def add_massive(self, models: Iterable[T]) -> list[T]:
        raise NotImplementedError


class EditService[T](EmptyService, ABC):
    async def edit(self, model: T) -> T:
        raise NotImplementedError


class DeleteService[T](EmptyService, ABC):
    async def delete(self, model: T) -> None:
        raise NotImplementedError


class GenericService[T](
    GetService[T],
    AddService[T],
    EditService[T],
    DeleteService[T],
    ABC,
):
    pass
