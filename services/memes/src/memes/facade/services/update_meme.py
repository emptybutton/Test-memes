from dataclasses import dataclass
from uuid import UUID
from typing import TypeAlias

from memes.application.cases import update_meme
from memes.facade import adapters
from memes.periphery import loggers
from memes.periphery.envs import Env
from memes.periphery.db.sessions import postgres_session_factory


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
    gateway = adapters.gateways.MediaGateway(Env.media_host, Env.media_port, Env.media_ssl)

    async with postgres_session_factory() as session:
        result = await update_meme.perform(
            meme_id,
            meme_text,
            meme_image_name,
            meme_image_content,
            transaction=adapters.transactions.DBTransaction(session),
            memes=adapters.repos.DBMemes(session, page_size=20),
            gateway=gateway,
            logger=adapters.loggers.Logger(loggers.main_logger),
        )

    return OutputDTO(
        meme_id=result.meme.id,
        meme_text=result.meme.text,
        meme_image_name=result.image.name,
        meme_image_content=result.image.content,
    )
