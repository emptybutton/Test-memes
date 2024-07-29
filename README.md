## Как запустить локально
Склонируйте этот репозиторий:
```bash
git clone https://github.com/emptybutton/Test-memes.git
```

Установите права для `minio`:
```bash
docker compose -f ./Test-memes/docker-compose.dev.yml run -d --name meme-minio minio
docker exec -it meme-minio bash
mc ready local
mc admin user add local access-key secret-key
mc policy attach local readwrite --user access-key
exit
docker kill meme-minio
```

Создайте недостающие бакеты в `minio`:
```bash
docker compose -f ./Test-memes/docker-compose.dev.yml run media python src/media/presentation/scripts/setup.py
```

Установите структуру для базы данных:
```bash
docker compose -f ./Test-memes/docker-compose.dev.yml run memes alembic upgrade head
```

Запустите внутри `docker`:
```bash
docker compose -f ./Test-memes/docker-compose.dev.yml up
```

> [!TIP]
> Если вы выполнили все шаги, то при повторном запуске можете выполнить только последнюю команду.

## Функциональность проекта
Существует только одна сущность - мем, имеющая ID, текст и картинку.</br>
Клиенты могут устанавливать только текст и картинку, при этом публично могут считыватся только ID и текст.</br>
Картинки не могут быть удалены из хранилища, даже если их мем обновляется или удаляется.

### Публичное API
<img src="https://github.com/emptybutton/Test-memes/blob/main/assets/api-view.png?raw=true"/>

## Тесты
Покрыта вся бизнес-логика публичного сервиса.

## Время выполнения детальнее
Всего на проект было потрачено **18 часов**, из которых:
1. **14 часов** на написание обоих сервисов, тестов и исправление багов
2. **4 часа** на изучение и внедрения DI фреймворка и исправление багов

## Про сервисы
В папке отдельного сервиса находится файл `README.md`, который содержит описание этого сервиса.
