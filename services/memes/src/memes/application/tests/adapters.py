from copy import copy
from types import TracebackType
from typing import Iterable, AsyncIterable, Self, Type, Iterator
from uuid import UUID

from memes.application import ports
from memes.domain import entities, vos


class CounterLogger(ports.loggers.Logger):
    __media_is_not_working_log_count: int = 0

    @property
    def media_is_not_working_log_count(self) -> int:
        return self.__media_is_not_working_log_count

    def log_media_is_not_working(self) -> None:
        self.__media_is_not_working_log_count += 1


class InMemoryMemes(ports.repos.Memes):
    def __init__(self, memes: Iterable[entities.Meme] = tuple(), *, page_size: int) -> None:
        self.__memes = [copy(meme) for meme in memes]
        self.__before_transaction_memes = None
        self.__page_size = page_size

    def __iter__(self) -> Iterator[entities.Meme]:
        return iter(map(copy, self.__memes))

    def begin(self) -> None:
        self.__before_transaction_memes = copy(self.__memes)

    def rollback(self) -> None:
        assert self.__before_transaction_memes is not None
        self.__memes = self.__before_transaction_memes

    def commit(self) -> None:
        self.__before_transaction_memes = None

    async def add(self, meme: entities.Meme) -> None:
        self.__memes.append(copy(meme))

    async def find_by_id(self, id: UUID) -> entities.Meme | None:
        for meme in self.__memes:
            if meme.id == id:
                return copy(meme)

    async def find_on_page(self, page_number: int) -> AsyncIterable[entities.Meme]:
        start_offset = page_number * self.__page_size
        end_offset = start_offset + self.__page_size

        for meme in map(copy, self.__memes[start_offset:end_offset]):
            yield meme

    async def update(self, meme: entities.Meme) -> None:
        for old_meme_index, old_meme in enumerate(self.__memes):
            if meme.id == old_meme.id:
                self.__memes[old_meme_index] = copy(meme)

    async def remove(self, meme: entities.Meme) -> None:
        for old_meme_index, old_meme in enumerate(self.__memes):
            if meme.id == old_meme.id:
                self.__memes.remove(old_meme)


class InMemoryMemeTransaction(ports.transactions.Transaction):
    def __init__(self, memes: InMemoryMemes) -> None:
        self.__memes = memes

    async def __aenter__(self) -> Self:
        self.__memes.begin()

        return self

    async def __aexit__(
        self,
        error_type: Type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        if error is None:
            self.__memes.commit()
        else:
            self.__memes.rollback()

        return error is None


class InMemoryMediaGateway(ports.gateways.media.Gateway):
    def __init__(self, images: Iterable[vos.Image] = tuple()) -> None:
        self.__images = set(images)

    def __iter__(self) -> Iterator[vos.Image]:
        return iter(self.__images)

    async def add_image(self, image: vos.Image) -> None:
        self.__images.add(image)

    async def update_image(self, image: vos.Image) -> None:
        for old_image in self.__images:
            if image.name == old_image.name:
                self.__images.remove(old_image)
                self.__images.add(image)
                return

        self.__images.add(image)

    async def get_image_by_name(
        self,
        name: str,
    ) -> vos.Image | ports.gateways.media.ReceivingFailures:
        for image in self.__images:
            if image.name == name:
                return name

        return ports.gateways.media.ReceivingFailures.no_image

    async def remove_by_name(self, name: str) -> None:
        for image in tuple(self.__images):
            if image.name == name:
                self.__images.remove(image)


class NotWorkingMediaGateway(ports.gateways.media.Gateway):
    async def add_image(self, image: vos.Image) -> ports.gateways.media.AdditionFailures:
        return ports.gateways.media.AdditionFailures.media_is_not_working

    async def update_image(self, image: vos.Image) -> ports.gateways.media.AdditionFailures:
        return ports.gateways.media.AdditionFailures.media_is_not_working

    async def get_image_by_name(
        self,
        name: str,
    ) -> ports.gateways.media.ReceivingFailures:
        return ports.gateways.media.ReceivingFailures.media_is_not_working

    async def remove_by_name(self, name: str) -> ports.gateways.media.RemovingFailures:
        return ports.gateways.media.RemovingFailures.media_is_not_working


class BadMediaGateway(ports.gateways.media.Gateway):
    async def add_image(self, image: vos.Image) -> ports.gateways.media.AdditionFailures:
        return ports.gateways.media.AdditionFailures.unsupported_image_extension

    async def update_image(self, image: vos.Image) -> ports.gateways.media.AdditionFailures:
        return ports.gateways.media.AdditionFailures.unsupported_image_extension

    async def get_image_by_name(
        self,
        name: str,
    ) -> ports.gateways.media.ReceivingFailures:
        return ports.gateways.media.ReceivingFailures.no_image

    async def remove_by_name(self, name: str) -> ports.gateways.media.RemovingFailures:
        return ports.gateways.media.RemovingFailures.media_is_not_working
