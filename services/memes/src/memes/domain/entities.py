from dataclasses import dataclass, field
from uuid import UUID, uuid4

from memes.domain import vos


@dataclass(kw_only=True)
class Meme:
    id: UUID = field(default_factory=uuid4)
    text: str
    image_name: str

    def use(self, image: vos.Image) -> None:
        self.image_name = image.name
