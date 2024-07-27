from pytest import mark, raises

from memes.application.cases import add_meme
from memes.application.tests import adapters


@mark.asyncio
async def test_valid_case() -> None:
    memes = adapters.InMemoryMemes(page_size=3)
    media_gateway = adapters.InMemoryMediaGateway()
    logger = adapters.CounterLogger()

    result = await add_meme.perform(
        "meme_text",
        "meme_image_name.png",
        b"meme_image_content",
        memes=memes,
        transaction=adapters.InMemoryMemeTransaction(memes),
        media_gateway=media_gateway,
        logger=logger,
    )

    assert logger.media_is_not_working_log_count == 0

    assert result.meme.text == "meme_text"
    assert result.meme.image_name == "meme_image_name.png"
    assert result.image.name == "meme_image_name.png"
    assert result.image.content == b"meme_image_content"

    stored_memes = tuple(memes)
    assert len(stored_memes) == 1
    stored_meme = stored_memes[0]

    assert stored_meme == result.meme

    stored_images = tuple(media_gateway)
    assert len(stored_images) == 1
    stored_image = stored_images[0]

    assert result.image == stored_image

    await add_meme.perform(
        "meme_text",
        "meme_image_name_1.png",
        b"meme_image_content",
        memes=memes,
        transaction=adapters.InMemoryMemeTransaction(memes),
        media_gateway=media_gateway,
        logger=logger,
    )

    assert len(tuple(memes)) == 2
    assert len(tuple(media_gateway)) == 2


@mark.asyncio
async def test_with_not_working_media() -> None:
    memes = adapters.InMemoryMemes(page_size=3)
    media_gateway = adapters.NotWorkingMediaGateway()
    logger = adapters.CounterLogger()

    with raises(add_meme.MediaIsNotWorkingError):
        await add_meme.perform(
            "meme_text",
            "meme_image_name.png",
            b"meme_image_content",
            memes=memes,
            transaction=adapters.InMemoryMemeTransaction(memes),
            media_gateway=media_gateway,
            logger=logger,
        )

    assert len(tuple(memes)) == 0
    assert logger.media_is_not_working_log_count == 1


@mark.asyncio
async def test_with_bad_media() -> None:
    memes = adapters.InMemoryMemes(page_size=3)
    media_gateway = adapters.BadMediaGateway()
    logger = adapters.CounterLogger()

    with raises(add_meme.UnsupportedImageExtensionError):
        await add_meme.perform(
            "meme_text",
            "meme_image_name.png",
            b"meme_image_content",
            memes=memes,
            transaction=adapters.InMemoryMemeTransaction(memes),
            media_gateway=media_gateway,
            logger=logger,
        )

    assert len(tuple(memes)) == 0
    assert logger.media_is_not_working_log_count == 0
