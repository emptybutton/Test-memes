import io

from media.infrastructure.periphery.minio.clients import client
from media.model.data.values import Bucket, File


async def exists(bucket: Bucket) -> bool:
    return client.bucket_exists(bucket.value)


async def make(bucket: Bucket) -> None:
    client.make_bucket(bucket.value)


async def put_in(bucket: Bucket, file: File) -> None:
    client.put_object(
        bucket.value,
        file.name,
        io.BytesIO(file.content),
        len(file.content),
    )


async def remove_from(bucket: Bucket, name: str) -> None:
    client.remove_object(bucket.value, name)


async def get_from(bucket: Bucket, name: str) -> File:
    try:
        response = client.get_object(bucket.value, name)
        return File(name=name, content=response.content)
    finally:
        response.close()
        response.release_conn()
