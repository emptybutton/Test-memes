from uuid import uuid4

from pytest import mark, raises

from memes.application.cases import update_meme
from memes.application.tests import adapters
from memes.domain import entities


@mark.asyncio
async def test_valid_case() -> None:
    meme1 = entities.Meme(text="text0", image_name="name0")
    meme2 = entities.Meme(text="text1", image_name="name1")

    memes = adapters.InMemoryMemes((meme1, meme2), page_size=3)
    transaction = adapters.InMemoryMemeTransaction(memes)
    media_gateway = adapters.InMemoryMediaGateway()
    logger = adapters.CounterLogger()

    result = await update_meme.perform(
        meme1.id,
        "new text",
        "new image name",
        b"new image content",
        transaction=transaction,
        memes=memes,
        media_gateway=media_gateway,
        logger=logger,
    )

    new_meme1 = await memes.find_by_id(meme1.id)
    assert new_meme1 is not None
    assert new_meme1.id == meme1.id
    assert new_meme1 == result.meme
    assert new_meme1.text == "new text"
    assert new_meme1.image_name == "new image name"

    uptodate_meme2 = await memes.find_by_id(meme2.id)
    assert uptodate_meme2 is not None
    assert uptodate_meme2 == meme2

    stored_images = tuple(media_gateway)
    assert len(stored_images) == 1

    new_image = stored_images[0]

    assert new_meme1.image_name == "new image name"
    assert new_meme1.image_name == new_image.name
    assert new_image.content == b"new image content"

    assert new_image == result.image

    assert logger.media_is_not_working_log_count == 0

    result2 = await update_meme.perform(
        meme_id=new_meme1.id,
        meme_text="second new text",
        meme_image_name="second new image name",
        meme_image_content=b"second new image content",
        transaction=transaction,
        memes=memes,
        media_gateway=media_gateway,
        logger=logger,
    )

    new_new_meme1 = await memes.find_by_id(new_meme1.id)
    assert new_new_meme1 is not None

    assert new_new_meme1.text == "second new text"
    assert new_new_meme1.image_name == "second new image name"

    stored_images = tuple(media_gateway)
    assert len(stored_images) == 2


@mark.asyncio
async def test_without_meme() -> None:
    meme1 = entities.Meme(text="text0", image_name="name0")

    memes = adapters.InMemoryMemes([meme1], page_size=3)
    transaction = adapters.InMemoryMemeTransaction(memes)
    media_gateway = adapters.InMemoryMediaGateway()
    logger = adapters.CounterLogger()

    with raises(update_meme.NoMemeError):
        await update_meme.perform(
            uuid4(),
            "new text",
            "new image name",
            b"new image content",
            transaction=transaction,
            memes=memes,
            media_gateway=media_gateway,
            logger=logger,
        )

    assert len(tuple(memes)) == 1

    new_meme1 = await memes.find_by_id(meme1.id)
    assert new_meme1 is not None
    assert meme1 == new_meme1


@mark.asyncio
async def test_with_not_working_media() -> None:
    meme1 = entities.Meme(text="text0", image_name="name0")

    memes = adapters.InMemoryMemes([meme1], page_size=3)
    transaction = adapters.InMemoryMemeTransaction(memes)
    media_gateway = adapters.NotWorkingMediaGateway()
    logger = adapters.CounterLogger()

    with raises(update_meme.MediaIsNotWorkingError):
        await update_meme.perform(
            meme_id=meme1.id,
            meme_text="new text",
            meme_image_name="new image name",
            meme_image_content=b"new image content",
            transaction=transaction,
            memes=memes,
            media_gateway=media_gateway,
            logger=logger,
        )

    assert len(tuple(memes)) == 1
    new_meme1 = await memes.find_by_id(meme1.id)
    assert new_meme1 is not None
    assert meme1 == new_meme1
    assert meme1.text == "text0"
    assert logger.media_is_not_working_log_count == 1


@mark.asyncio
async def test_with_bad_media() -> None:
    meme1 = entities.Meme(text="text0", image_name="name0")

    memes = adapters.InMemoryMemes([meme1], page_size=3)
    transaction = adapters.InMemoryMemeTransaction(memes)
    media_gateway = adapters.BadMediaGateway()
    logger = adapters.CounterLogger()

    with raises(update_meme.UnsupportedImageExtensionError):
        await update_meme.perform(
            meme1.id,
            "new text",
            "new image name",
            b"new image content",
            transaction=transaction,
            memes=memes,
            media_gateway=media_gateway,
            logger=logger,
        )

    assert len(tuple(memes)) == 1
    new_meme1 = await memes.find_by_id(meme1.id)
    assert new_meme1 is not None
    assert meme1 == new_meme1
    assert meme1.text == "text0"
