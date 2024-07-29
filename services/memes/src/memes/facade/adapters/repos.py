from typing import AsyncIterator
from uuid import UUID

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from memes.application.ports import repos
from memes.domain import entities
from memes.periphery.db import tables


class DBMemes(repos.Memes):
    def __init__(self, session: AsyncSession, *, page_size: int) -> None:
        self.__session = session
        self.__page_size = page_size
        assert self.__page_size > 0

    async def add(self, meme: entities.Meme) -> None:
        stmt = insert(tables.Meme).values(
            id=meme.id,
            text=meme.text,
            image_name=meme.image_name,
        )

        await self.__session.execute(stmt)

    async def find_by_id(self, id: UUID) -> entities.Meme | None:
        query = (
            select(
                tables.Meme.text,
                tables.Meme.image_name,
            )
            .where(tables.Meme.id == id)
            .limit(1)
        )

        results = await self.__session.execute(query)
        raw_meme = results.first()

        if raw_meme is None:
            return None

        return entities.Meme(
            id=id,
            text=raw_meme.text,
            image_name=raw_meme.image_name,
        )

    async def find_on_page(self, page_number: int) -> AsyncIterator[entities.Meme]:
        query = (
            select(
                tables.Meme.id,
                tables.Meme.text,
                tables.Meme.image_name,
            )
            .offset(self.__page_size * page_number)
            .limit(self.__page_size)
        )

        results = await self.__session.execute(query)

        for result in results.all():
            yield self.__meme_of(result)

    def __meme_of(self, raw_meme: object) -> entities.Meme:
        return entities.Meme(
            id=raw_meme.id,
            text=raw_meme.text,
            image_name=raw_meme.image_name,
        )

    async def update(self, meme: entities.Meme) -> None:
        stmt = (
            update(tables.Meme)
            .where(tables.Meme.id == meme.id)
            .values(
                text=meme.text,
                image_name=meme.image_name,
            )
        )

        await self.__session.execute(stmt)

    async def remove(self, meme: entities.Meme) -> None:
        stmt = delete(tables.Meme).where(tables.Meme.id == meme.id)
        await self.__session.execute(stmt)
