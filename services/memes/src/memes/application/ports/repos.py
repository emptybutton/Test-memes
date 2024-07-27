from abc import ABC, abstractmethod
from typing import AsyncIterable
from uuid import UUID

from memes.domain.entities import Meme


class Memes(ABC):
    @abstractmethod
    async def add(self, meme: Meme) -> None: ...

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Meme | None: ...

    @abstractmethod
    async def find_on_page(self, page_number: int) -> AsyncIterable[Meme]: ...

    @abstractmethod
    async def update(self, meme: Meme) -> None: ...

    @abstractmethod
    async def remove(self, meme: Meme) -> None: ...
