FROM sunpeek/poetry:py3.12-slim

WORKDIR /media

ENV PYTHONPATH /media/src
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml .
COPY poetry.lock .
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-root

COPY . .

ENTRYPOINT ["poetry", "run"]
CMD ["ash"]
