import typenv


_env = typenv.Env()
_env.read_env(".env", override=True)


class Env:
    public_url = _env.str("PUBLIC_URL")

    media_ssl = _env.bool("MEDIA_SSL")
    media_host = _env.str("MEDIA_HOST")
    media_port = _env.int("MEDIA_PORT")

    postgres_database = _env.str("POSTGRES_DATABASE")
    postgres_username = _env.str("POSTGRES_USER")
    postgres_password = _env.str("POSTGRES_PASSWORD")
    postgres_host = _env.str("POSTGRES_HOST")
    postgres_port = _env.int("POSTGRES_PORT")
    postgres_echo = _env.bool("POSTGRES_ECHO")
