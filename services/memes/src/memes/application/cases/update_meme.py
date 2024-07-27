from dataclasses import dataclass
from uuid import UUID

from memes.domain import entities, vos
from memes.application import ports


@dataclass(kw_only=True, frozen=True)
class OutputDTO:
    meme: entities.Meme
    image: vos.Image


class BaseError(Exception): ...


class NoMemeError(BaseError): ...


class MediaIsNotWorkingError(BaseError): ...


class UnsupportedImageExtensionError(BaseError): ...


async def perform(
    meme_id: UUID,
    meme_text: str,
    meme_image_name: str,
    meme_image_content: bytes,
    *,
    transaction: ports.transactions.Transaction,
    memes: ports.repos.Memes,
    media_gateway: ports.gateways.media.Gateway,
    logger: ports.loggers.Logger,
) -> OutputDTO:
    new_meme_image = vos.Image(name=meme_image_name, content=meme_image_content)

    async with transaction:
        meme = await memes.find_by_id(meme_id)

        if meme is None:
            raise NoMemeError

        meme.text = meme_text
        meme.use(new_meme_image)

        await memes.update(meme)

        result = await media_gateway.update_image(new_meme_image)

        if result is ports.gateways.media.AdditionFailures.media_is_not_working:
            logger.log_media_is_not_working()
            raise MediaIsNotWorkingError

        if result is ports.gateways.media.AdditionFailures.unsupported_image_extension:
            raise UnsupportedImageExtensionError

    return OutputDTO(meme=meme, image=new_meme_image)
