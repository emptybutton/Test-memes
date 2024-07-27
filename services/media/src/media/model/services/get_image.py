from media.infrastructure.facade import s3
from media.model.data.values import Bucket, File


async def perform(name: str) -> File | None:
    image = await s3.get_from(Bucket.images, name)

    return None if image is None or not image.is_image else image
