import typenv


_env = typenv.Env()
_env.read_env(".env", override=True)


class Env:
    minio_server = _env.str("MINIO_SERVER")
    minio_access_key = _env.str("MINIO_ACCESS_KEY")
    minio_secret_key = _env.str("MINIO_SECRET_KEY")
    minio_ssl = _env.bool("MINIO_SSL")
