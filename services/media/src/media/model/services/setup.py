from media.infrastructure.facade import s3
from media.model.data.values import Bucket


async def perform() -> None:
    for bucket in Bucket:
        if not await s3.exists(bucket):
            await s3.make(bucket)
