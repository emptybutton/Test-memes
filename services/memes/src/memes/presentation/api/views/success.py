from uuid import UUID
from typing import Self

from pydantic import BaseModel
from memes.periphery.envs import Env


class MemeView(BaseModel):
    meme_id: UUID
    meme_text: str


class MemeListView(BaseModel):
    next_page_url: str
    previous_page_url: str | None
    memes: list[MemeView]

    @classmethod
    def of(cls, meme_page: list[MemeView], page_number: int) -> Self:
        next_page_url = cls.__page_url_with(page_number + 1)
        previous_page_url = (
            None if page_number == 0 else cls.__page_url_with(page_number - 1)
        )

        return cls(
            next_page_url=next_page_url,
            previous_page_url=previous_page_url,
            memes=meme_page,
        )

    @staticmethod
    def __page_url_with(page_number: int) -> str:
        return f"{Env.public_url}/memes?page_number={page_number}"
