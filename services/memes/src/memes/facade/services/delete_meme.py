from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID

from memes.application.cases import delete_meme
from memes.facade import adapters
from memes.facade.di.containers import adapter_container


@dataclass(kw_only=True, frozen=True)
class OutputDTO:
    meme_id: UUID
    meme_text: str
    meme_image_name: str


BaseError: TypeAlias = delete_meme.BaseError

NoMemeError: TypeAlias = delete_meme.NoMemeError


async def perform(meme_id: UUID) -> OutputDTO:
    async with adapter_container() as container:
        meme = await delete_meme.perform(
            meme_id,
            transaction=await container.get(adapters.transactions.DBTransaction),
            memes=await container.get(adapters.repos.DBMemes),
        )

    return OutputDTO(
        meme_id=meme.id,
        meme_text=meme.text,
        meme_image_name=meme.image_name,
    )
