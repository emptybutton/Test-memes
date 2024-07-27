from media.infrastructure.facade import s3
from media.model.data.values import Bucket, File


class NotImageError(Exception): ...


async def perform(data: bytes, name: str) -> None:
    image = File(name=name, content=data)

    if not image.is_image:
        raise NotImageError

    await s3.put_in(Bucket.images, image)
