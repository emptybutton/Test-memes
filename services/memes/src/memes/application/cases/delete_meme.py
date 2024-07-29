from uuid import UUID

from memes.domain import entities
from memes.application import ports


class BaseError(Exception): ...


class NoMemeError(BaseError): ...


async def perform(
    meme_id: UUID,
    *,
    transaction: ports.transactions.Transaction,
    memes: ports.repos.Memes,
) -> entities.Meme:
    async with transaction:
        meme = await memes.find_by_id(meme_id)

        if meme is None:
            raise NoMemeError

        await memes.remove(meme)

    return meme
