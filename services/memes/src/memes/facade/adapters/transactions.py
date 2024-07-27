from typing import Type, Self
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from memes.application.ports import transactions


class DBTransaction(transactions.Transaction):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def __aenter__(self) -> Self:
        await self.session.begin_nested()

        return self

    async def __aexit__(
        self,
        error_type: Type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        if error is None:
            await self.session.commit()
        else:
            await self.session.rollback()

        return error is None
