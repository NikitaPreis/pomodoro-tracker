# Pomodoro-tracker

### Описание

Проект «pomodoro-tracker» — это микросервис для работы с помодоро-трекером.
В сервисе реализованы следующие функции:
1. Создание, обновление, удаление и получение задач;
2. Авторизация и аутентификация на JWT-токенах;
3. Авторизация и аутентификация с Google API;
4. Настроено кэширование задач с Redis.

### Стек технологий:

* Python (3.11.9)
* FastAPI
* Pydantic
* Starlette
* Uvicorn
* SQLAlchemy
* Alembic
* PostgreSQL
* Redis
* Docker

### Как развернуть проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git@github.com:NikitaPreis/insta-service.git
cd insta-service
```

Создать и активировать виртуальное окружение, установить зависимости с помощью Poetry.

Установить переменные окружения в файле .env:
```
# Переменные окружения для работы с БД (Docker Compose, PostgreSQL)
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_USER=postgres
POSTGRES_DB=pomodoro
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Переменные окружения для работы с БД (SQLAlchemy, Alembic):
DB_DRIVER=postgresql+psycopg2
DB_PASSWORD=mysecretpassword
DB_USER=postgres
DB_NAME=pomodoro
DB_HOST=localhost
DB_PORT=5432

# Переменные окружжения для работы с Google API:
GOOGLE_TOKEN_ID=<google-token-id>
GOOGLE_CLIENT_ID=<google-client-id>
GOOGLE_CLIENT_SECRET=<google-client-secret>
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google

```

Запустить Docker daemon и ввести команду для запуска БД (PostgreSQL) в контейнере через Docker Compose:
```
docker compose up
```

Запустить сервер, создать и выполнить миграции:
```
fab makemigrations
fab migrate
fab runserver
```

Документация будет доступна по адресу: 

* http://localhost:8000/docs
