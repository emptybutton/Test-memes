from uuid import uuid4

from pytest import mark

from memes.application.cases import read_meme
from memes.application.tests import adapters
from memes.domain import entities


@mark.asyncio
async def test_valid_case() -> None:
    meme = entities.Meme(text="text", image_name="name")
    memes = adapters.InMemoryMemes([meme], page_size=3)

    result = await read_meme.perform(
        uuid4(),
        memes=memes,
        transaction=adapters.InMemoryMemeTransaction(memes),
    )
    assert result is None

    result = await read_meme.perform(
        meme.id,
        memes=memes,
        transaction=adapters.InMemoryMemeTransaction(memes),
    )
    assert result == meme
