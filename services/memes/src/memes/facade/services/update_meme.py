from dataclasses import dataclass
from uuid import UUID
from typing import TypeAlias

from memes.application.cases import update_meme
from memes.facade import adapters
from memes.facade.di.containers import adapter_container


@dataclass(kw_only=True, frozen=True)
class OutputDTO:
    meme_id: UUID
    meme_text: str
    meme_image_name: str
    meme_image_content: bytes


BaseError: TypeAlias = update_meme.BaseError

NoMemeError: TypeAlias = update_meme.NoMemeError

MediaIsNotWorkingError: TypeAlias = update_meme.MediaIsNotWorkingError

UnsupportedImageExtensionError: TypeAlias = update_meme.UnsupportedImageExtensionError


async def perform(
    meme_id: UUID,
    meme_text: str,
    meme_image_name: str,
    meme_image_content: bytes,
) -> OutputDTO:
    async with adapter_container() as container:
        result = await update_meme.perform(
            meme_id,
            meme_text,
            meme_image_name,
            meme_image_content,
            transaction=await container.get(adapters.transactions.DBTransaction),
            memes=await container.get(adapters.repos.DBMemes),
            media_gateway=await container.get(adapters.gateways.MediaGateway),
            logger=await container.get(adapters.loggers.Logger),
        )

    return OutputDTO(
        meme_id=result.meme.id,
        meme_text=result.meme.text,
        meme_image_name=result.image.name,
        meme_image_content=result.image.content,
    )
