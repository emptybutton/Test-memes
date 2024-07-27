from dataclasses import dataclass
from typing import AsyncIterable

from memes.domain import entities
from memes.application import ports


@dataclass(kw_only=True, frozen=True)
class OutputDTO:
    page_memes: AsyncIterable[entities.Meme]
    page_number: int


class BaseError(Exception): ...


class NegativePageNumberError(BaseError): ...


async def perform(
    page_number: int | None,
    *,
    transaction: ports.transactions.Transaction,
    memes: ports.repos.Memes,
) -> OutputDTO:
    if page_number is None:
        page_number = 0
    elif page_number < 0:
        raise NegativePageNumberError

    async with transaction:
        page_memes = memes.find_on_page(page_number)

    return OutputDTO(
        page_memes=page_memes,
        page_number=page_number,
    )
