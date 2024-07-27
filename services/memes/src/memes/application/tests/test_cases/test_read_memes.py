from asyncio import gather

from pytest import mark, raises

from memes.application.cases import read_memes
from memes.application.tests import adapters
from memes.domain import entities


@mark.asyncio
async def test_cases() -> None:
    stored_memes = [
        entities.Meme(text=f"text{i}", image_name=f"name{i}")
        for i in range(190)
    ]
    memes = adapters.InMemoryMemes(stored_memes, page_size=50)
    transaction = adapters.InMemoryMemeTransaction(memes)

    result0 = await read_memes.perform(None, memes=memes, transaction=transaction)
    assert result0.page_number == 0
    result0_memes = [meme async for meme in result0.page_memes]
    assert len(result0_memes) == 50

    result0_1 = await read_memes.perform(0, memes=memes, transaction=transaction)
    assert result0_1.page_number == 0
    assert all([
        meme in result0_memes
        async for meme in result0.page_memes
    ])

    result1 = await read_memes.perform(1, memes=memes, transaction=transaction)
    assert result1.page_number == 1
    assert len([meme async for meme in result1.page_memes]) == 50

    result2 = await read_memes.perform(2, memes=memes, transaction=transaction)
    assert result2.page_number == 2
    assert len([meme async for meme in result2.page_memes]) == 50

    result3 = await read_memes.perform(3, memes=memes, transaction=transaction)
    assert result3.page_number == 3
    assert len([meme async for meme in result3.page_memes]) == 40

    result4 = await read_memes.perform(4, memes=memes, transaction=transaction)
    assert result4.page_number == 4
    assert len([meme async for meme in result4.page_memes]) == 0

    result100 = await read_memes.perform(100, memes=memes, transaction=transaction)
    assert result100.page_number == 100
    assert len([meme async for meme in result100.page_memes]) == 0

    with raises(read_memes.NegativePageNumberError):
        async for _ in await read_memes.perform(-5, memes=memes, transaction=transaction):
            ...
