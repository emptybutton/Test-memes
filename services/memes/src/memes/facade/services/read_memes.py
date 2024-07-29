from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID

from memes.application.cases import read_memes
from memes.facade import adapters
from memes.facade.di.containers import adapter_container


@dataclass(kw_only=True, frozen=True)
class MemeDTO:
    meme_id: UUID
    meme_text: str
    meme_image_name: str


@dataclass(kw_only=True, frozen=True)
class OutputDTO:
    page_memes: tuple[MemeDTO, ...]
    page_number: int


BaseError: TypeAlias = read_memes.BaseError

NegativePageNumberError: TypeAlias = read_memes.NegativePageNumberError


async def perform(page_number: int | None) -> OutputDTO:
    async with adapter_container() as container:
        result = await read_memes.perform(
            page_number,
            transaction=await container.get(adapters.transactions.DBTransaction),
            memes=await container.get(adapters.repos.DBMemes),
        )

        page_memes = list()

        async for page_meme in result.page_memes:
            page_memes.append(MemeDTO(
                meme_id=page_meme.id,
                meme_text=page_meme.text,
                meme_image_name=page_meme.image_name,
            ))

        return OutputDTO(
            page_memes=tuple(page_memes),
            page_number=result.page_number,
        )
