# Pomodoro-tracker

### Описание

Проект «pomodoro-tracker» — это микросервис для работы с помодоро-трекером.
В сервисе реализованы следующие функции:
1. Создание, обновление, удаление и получение задач;
2. Авторизация и аутентификация на JWT-токенах;
3. Авторизация и аутентификация с Google API (OAuth 2.0);
4. Авторизация и аутентификация с API Яндекс ID (OAuth 2.0);
5. Настроено кэширование задач с Redis.

### Стек технологий:

* Python (3.11.9)
* FastAPI
* Pydantic
* Starlette
* Uvicorn
* HTTPX
* Pytest
* SQLAlchemy
* Alembic
* PostgreSQL
* Redis
* Docker

### Как развернуть проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git@github.com:NikitaPreis/pomodoro-tracker.git
cd pomodoro-tracker
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

# Переменные окружения для работы с тестовой БД (SQLAlchemy):
TEST_DB_NAME=pomodoro-test

# Переменные окружжения для работы с Google API:
GOOGLE_TOKEN_ID=<google-token-id>
GOOGLE_CLIENT_ID=<google-client-id>
GOOGLE_CLIENT_SECRET=<google-client-secret>
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google

# Переменные окружжения для работы с API Яндекс ID:
YANDEX_CLIENT_ID=<yandex-client-id>
YANDEX_CLIENT_SECRET=<yandex-client-secret>
YANDEX_REDIRECT_URI=http://localhost:8000/auth/yandex

```

Установить переменные окружения в файле .test.env:
```
# Переменные окружения для работы с тестовой БД (Docker Compose, PostgreSQL)
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_USER=postgres
POSTGRES_DB=pomodoro-test
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

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


### Как проверить работу сервиса с помощью тестов:
* Убедитесь, что вы установили переменные окружения для тестовой базы данных в файле .test.env
* Запустите тестовую базу данных: `docker compose -f docker-compose.test.yml up`
* Выполните подходящую команду из корневой директории:
1. Для запуска всех тестов: `pytest`
2. Для запуска unit-тестов и компонетных тестов: `pytest tests/unit/`
3. Для запуска интеграционных: `pytest tests/integration/`

### Проект находится на стадии разработки

**Ведется работа по направлениям:**
- реализация микросервиса для работы с аналитикой;
- реализация работы с фоновыми задачами (Celery, Redis, RabbitMQ);
- реализация взаимодействия микросервисов (Celery, RabbitMQ, Kafka).
