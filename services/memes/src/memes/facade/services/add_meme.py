from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID

from memes.application.cases import add_meme
from memes.facade import adapters
from memes.periphery.envs import Env
from memes.periphery.db.sessions import postgres_session_factory
from memes.periphery import loggers


@dataclass(kw_only=True, frozen=True)
class OutputDTO:
    meme_id: UUID
    meme_text: str
    meme_image_name: str
    meme_image_content: bytes


BaseError: TypeAlias = add_meme.BaseError

MediaIsNotWorkingError: TypeAlias = add_meme.MediaIsNotWorkingError

UnsupportedImageExtensionError: TypeAlias = add_meme.UnsupportedImageExtensionError


async def perform(
    meme_text: str,
    meme_image_name: str,
    meme_image_content: bytes,
) -> OutputDTO:
    gateway = adapters.gateways.MediaGateway(Env.media_host, Env.media_port, Env.media_ssl)

    async with postgres_session_factory() as session:
        result = await add_meme.perform(
            meme_text,
            meme_image_name,
            meme_image_content,
            transaction=adapters.transactions.DBTransaction(session),
            memes=adapters.repos.DBMemes(session, page_size=20),
            media_gateway=gateway,
            logger=adapters.loggers.Logger(loggers.main_logger),
        )

    return OutputDTO(
        meme_id=result.meme.id,
        meme_text=result.meme.text,
        meme_image_name=result.image.name,
        meme_image_content=result.image.content,
    )
