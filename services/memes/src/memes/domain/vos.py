from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class Image:
    name: str
    content: bytes
