from dataclasses import dataclass
from uuid import UUID

from memes.application.cases import read_meme
from memes.facade import adapters
from memes.periphery.db.sessions import postgres_session_factory


@dataclass(kw_only=True, frozen=True)
class OutputDTO:
    meme_id: UUID
    meme_text: str
    meme_image_name: str


async def perform(meme_id: UUID) -> OutputDTO:
    async with postgres_session_factory() as session:
        result = await read_meme.perform(
            meme_id,
            transaction=adapters.transactions.DBTransaction(session),
            memes=adapters.repos.DBMemes(session, page_size=20),
        )

    return OutputDTO(
        meme_id=result.meme.id,
        meme_text=result.meme.text,
        meme_image_name=result.image.name,
    )
