from uuid import UUID

from memes.domain import entities
from memes.application import ports


async def perform(
    meme_id: UUID,
    *,
    transaction: ports.transactions.Transaction,
    memes: ports.repos.Memes,
) -> entities.Meme | None:
    async with transaction:
        return await memes.find_by_id(meme_id)
