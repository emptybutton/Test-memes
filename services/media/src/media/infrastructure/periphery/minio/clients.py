from minio import Minio

from media.infrastructure.periphery.envs import Env


client = Minio(
    endpoint=Env.minio_server,
    access_key=Env.minio_access_key,
    secret_key=Env.minio_secret_key,
)
