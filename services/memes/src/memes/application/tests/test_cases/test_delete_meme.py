from uuid import uuid4

from pytest import mark, raises

from memes.application.cases import delete_meme
from memes.application.tests import adapters
from memes.domain import entities, vos


@mark.asyncio
async def test_without_meme() -> None:
    memes = adapters.InMemoryMemes(page_size=3)
    media_gateway = adapters.InMemoryMediaGateway()
    logger = adapters.CounterLogger()

    with raises(delete_meme.NoMemeError):
        await delete_meme.perform(
            uuid4(),
            memes=memes,
            transaction=adapters.InMemoryMemeTransaction(memes),
            media_gateway=media_gateway,
            logger=logger,
        )

    assert len(tuple(memes)) == 0
    assert len(tuple(media_gateway)) == 0
    assert logger.media_is_not_working_log_count == 0


@mark.asyncio
async def test_valid_case() -> None:
    first_meme = entities.Meme(text="text", image_name="name")
    second_meme = entities.Meme(text="text1", image_name="name1")
    image = vos.Image(name="name1", content=b"content")

    memes = adapters.InMemoryMemes([first_meme, second_meme], page_size=3)
    media_gateway = adapters.InMemoryMediaGateway([image])
    logger = adapters.CounterLogger()

    await delete_meme.perform(
        first_meme.id,
        memes=memes,
        transaction=adapters.InMemoryMemeTransaction(memes),
        media_gateway=media_gateway,
        logger=logger,
    )

    assert len(tuple(memes)) == 1
    assert len(tuple(media_gateway)) == 1
    assert logger.media_is_not_working_log_count == 0

    await delete_meme.perform(
        second_meme.id,
        memes=memes,
        transaction=adapters.InMemoryMemeTransaction(memes),
        media_gateway=media_gateway,
        logger=logger,
    )

    assert len(tuple(memes)) == 0
    assert len(tuple(media_gateway)) == 0
    assert logger.media_is_not_working_log_count == 0


@mark.asyncio
async def test_with_not_working_media() -> None:
    meme = entities.Meme(text="text", image_name="name")
    memes = adapters.InMemoryMemes([meme], page_size=3)
    logger = adapters.CounterLogger()

    with raises(delete_meme.MediaIsNotWorkingError):
        await delete_meme.perform(
            meme.id,
            memes=memes,
            transaction=adapters.InMemoryMemeTransaction(memes),
            media_gateway=adapters.NotWorkingMediaGateway(),
            logger=logger,
        )

    assert len(tuple(memes)) == 1
    assert logger.media_is_not_working_log_count == 1
