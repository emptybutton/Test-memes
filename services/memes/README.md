# Memes
Cервис с публичным API и основной бизнес-логикой.

## Внутри
Написан по ЧА.</br>
Стек:
- `fastapi` для api
- `dishka` для DI
- `aiohttp` для взаимодействия с api других сервисов (`Media`)
- `sqlalchemy` для взаимодействия с БД (СУБД - `Postgres`)
- `pytest` для тестов

## Почему так
Имеет Core домен, и если расширение будет не в виде новых сервисов, то, скорее всего, в виде расширения этого.
