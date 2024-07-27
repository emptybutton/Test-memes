from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        return f"db.{type(self).__name__}(id={self.id!r})"


class Meme(Base):
    __tablename__ = "memes"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    text: Mapped[str]
    image_name: Mapped[str]
