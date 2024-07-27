from dataclasses import dataclass

from memes.domain import entities, vos
from memes.application import ports


@dataclass(kw_only=True, frozen=True)
class OutputDTO:
    meme: entities.Meme
    image: vos.Image


class BaseError(Exception): ...


class MediaIsNotWorkingError(BaseError): ...


class UnsupportedImageExtensionError(BaseError): ...


async def perform(
    meme_text: str,
    meme_image_name: str,
    meme_image_content: bytes,
    *,
    transaction: ports.transactions.Transaction,
    memes: ports.repos.Memes,
    media_gateway: ports.gateways.media.Gateway,
    logger: ports.loggers.Logger,
) -> OutputDTO:
    meme_image = vos.Image(name=meme_image_name, content=meme_image_content)
    meme = entities.Meme(text=meme_text, image_name=meme_image.name)

    async with transaction:
        await memes.add(meme)

        result = await media_gateway.add_image(meme_image)

        if result is ports.gateways.media.AdditionFailures.media_is_not_working:
            logger.log_media_is_not_working()
            raise MediaIsNotWorkingError

        if result is ports.gateways.media.AdditionFailures.unsupported_image_extension:
            raise UnsupportedImageExtensionError

    return OutputDTO(meme=meme, image=meme_image)
