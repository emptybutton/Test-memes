# Результат тестового задания
Реализованны:
1. телеграм-бот для конечных пользователей, написанный на `aiogram`
2. полу-рак, полу-микросервис на `FastAPI`

Можно запустить при помощи команд:
```bash
git clone https://github.com/emptybutton/Test-bot.git
docker compose --project-directory ./Test-bot up
```

## Телеграм-бот
Запрашивает у пользователя два числа и отправляет их в FastAPI-приложение для "вычисления":

<img src="https://github.com/emptybutton/Test-bot/blob/main/assets/dialog.png?raw=true"/>

## API приложения
Имеет один эндпоинт для сложения двух чисел:

<img src="https://github.com/emptybutton/Test-bot/blob/main/assets/api.png?raw=true"/>
