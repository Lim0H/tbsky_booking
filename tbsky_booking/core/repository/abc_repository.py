from abc import ABC
from typing import Generator, Iterable, Optional

__all__ = [
    "GetRepository",
    "AddRepository",
    "EditRepository",
    "DeleteRepository",
    "GenericRepository",
    "EmptyRepository",
]


class EmptyRepository[T](ABC):
    pass


class GetRepository[T](EmptyRepository, ABC):
    async def get(self, *args, **kwargs) -> list[T]:
        raise NotImplementedError

    async def get_iter(self, *args, **kwargs) -> Generator[T, None, None]:
        raise NotImplementedError

    async def get_dict_list(self, *args, **kwargs) -> dict[str, list[T]]:
        raise NotImplementedError

    async def get_dict(self, *args, **kwargs) -> dict[str, T]:
        return {k: v[0] for k, v in (await self.get_dict_list(*args, **kwargs)).items()}

    async def get_first(self, *args, **kwargs) -> Optional[T]:
        result = await self.get(*args, **kwargs)
        return result[0] if result else None

    async def get_one(self, *args, **kwargs) -> T:
        result = await self.get(*args, **kwargs)
        if result:
            return result[0]
        raise ValueError


class AddRepository[T](EmptyRepository, ABC):
    async def add(self, model: T) -> T:
        raise NotImplementedError

    async def add_massive(self, models: Iterable[T]) -> list[T]:
        raise NotImplementedError


class EditRepository[T](EmptyRepository, ABC):
    async def edit(self, model: T) -> T:
        raise NotImplementedError


class DeleteRepository[T](EmptyRepository, ABC):
    async def delete(self, model: T) -> None:
        raise NotImplementedError


class GenericRepository[T](
    GetRepository[T],
    AddRepository[T],
    EditRepository[T],
    DeleteRepository[T],
    ABC,
):
    pass
