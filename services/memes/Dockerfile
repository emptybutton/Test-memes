FROM sunpeek/poetry:py3.12-slim

WORKDIR /memes

ENV PYTHONPATH /memes/src
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml .
COPY poetry.lock .
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-root

COPY . .

ENTRYPOINT ["poetry", "run"]
CMD ["ash"]
