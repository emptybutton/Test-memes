from media.infrastructure.facade import s3
from media.model.data.values import Bucket


async def perform(name: str) -> None:
    await s3.remove_from(Bucket.images, name)
