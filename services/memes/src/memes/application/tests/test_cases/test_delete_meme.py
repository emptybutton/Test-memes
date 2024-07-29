from uuid import uuid4

from pytest import mark, raises

from memes.application.cases import delete_meme
from memes.application.tests import adapters
from memes.domain import entities


@mark.asyncio
async def test_without_meme() -> None:
    memes = adapters.InMemoryMemes(page_size=3)

    with raises(delete_meme.NoMemeError):
        await delete_meme.perform(
            uuid4(),
            memes=memes,
            transaction=adapters.InMemoryMemeTransaction(memes),
        )

    assert len(tuple(memes)) == 0


@mark.asyncio
async def test_valid_case() -> None:
    first_meme = entities.Meme(text="text", image_name="name")
    second_meme = entities.Meme(text="text1", image_name="name1")

    memes = adapters.InMemoryMemes([first_meme, second_meme], page_size=3)

    await delete_meme.perform(
        first_meme.id,
        memes=memes,
        transaction=adapters.InMemoryMemeTransaction(memes),
    )

    assert len(tuple(memes)) == 1

    await delete_meme.perform(
        second_meme.id,
        memes=memes,
        transaction=adapters.InMemoryMemeTransaction(memes),
    )

    assert len(tuple(memes)) == 0
