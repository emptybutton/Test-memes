from uuid import UUID

from memes.domain import entities
from memes.application import ports


class BaseError(Exception): ...


class NoMemeError(BaseError): ...


class MediaIsNotWorkingError(BaseError): ...


async def perform(
    meme_id: UUID,
    *,
    transaction: ports.transactions.Transaction,
    memes: ports.repos.Memes,
    media_gateway: ports.gateways.media.Gateway,
    logger: ports.loggers.Logger,
) -> entities.Meme:
    async with transaction:
        meme = await memes.find_by_id(meme_id)

        if meme is None:
            raise NoMemeError

        await memes.remove(meme)

        result = await media_gateway.remove_by_name(meme.image_name)

        if result is ports.gateways.media.RemovingFailures.media_is_not_working:
            logger.log_media_is_not_working()
            raise MediaIsNotWorkingError

    return meme
