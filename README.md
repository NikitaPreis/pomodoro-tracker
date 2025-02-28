# Pomodoro-tracker

### Описание

Проект «pomodoro-tracker» — это микросервис для работы с помодоро-трекером.
В сервисе реализованы следующие функции:
1. Создание, обновление, удаление и получение задач;
2. Авторизация и аутентификация на JWT-токенах;
3. Авторизация и аутентификация с Google API (OAuth 2.0);
4. Авторизация и аутентификация с API Яндекс ID (OAuth 2.0);
5. Подключена отправка приветственных сообщений после OAuth-авторизации через микросервис для отправки email (SMTP + Яндекс Почта, RabbitMQ + Microservice);
6. Настроено кэширование задач с Redis.

### Стек технологий:

* Python (3.11.9)
* FastAPI
* Pydantic
* HTTPX
* Pytest
* SQLAlchemy
* Alembic
* PostgreSQL
* Redis
* Celery
* RabbitMQ
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
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Переменные окружения для работы с БД (SQLAlchemy, Alembic):
DB_DRIVER=postgresql+asyncpg
DB_PASSWORD=mysecretpassword
DB_USER=postgres
DB_NAME=pomodoro
DB_HOST=db
DB_PORT=5432


# Переменные окружения для работы с тестовой БД (SQLAlchemy):
TEST_DB_NAME=pomodoro-test
TEST_DB_HOST=localhost
TEST_GOOGLE_USER_RECIPIENT_EMAIL=<email.recipient@gmail.com>  # Укажите действующую почту.


# Переменные окружжения для работы с Google API:
GOOGLE_TOKEN_ID=<google-token-id>
GOOGLE_CLIENT_ID=<google-client-id>
GOOGLE_CLIENT_SECRET=<google-client-secret>
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google

# Переменные окружжения для работы с API Яндекс ID:
YANDEX_CLIENT_ID=<yandex-client-id>
YANDEX_CLIENT_SECRET=<yandex-client-secret>
YANDEX_REDIRECT_URI=http://localhost:8000/auth/yandex

# Переменные окружения для отправки email через Яндекс Почту (SMTP):
# Документация по настройке Яндекс Почты:
# https://yandex.ru/support/yandex-360/business/mail/ru/mail-clients/others
FROM_EMAIL=<sender.email@yandex.ru>  # Разрешите доступ к почтовому ящику с помощью почтовых клиентов
SMTP_PORT=465
SMTP_HOST=smtp.yandex.ru
SMTP_PASSWORD=<new.password.for.app>  # Создайте пароль для приложения

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


Запустить проект через Docker-Compose:
```
docker compose -f docker-compose.yml up --build
```

Создать и выполнить миграции в контейнере:
```
docker compose -f docker-compose.yml up --build
fab makemigrations
fab migrate
```

Документация будет доступна по адресу: 

* http://localhost:8000/docs

**ВАЖНО:** для полноценной работы сервиса требуется развернуть дополнительные сервисы:
1. Сервис для отправки сообщений на почту: https://github.com/NikitaPreis/pomodoro_mail_service.git


### Как проверить работу сервиса с помощью тестов:
* Убедитесь, что вы установили переменные окружения для тестовой базы данных в файле .test.env
* Установите значение переменной TESTING (str) на 'True' в конфигурации настроек `app.settings`
* Запустите тестовую базу данных: `docker compose -f docker-compose.test.yml up`
* Выполните подходящую команду из корневой директории:
1. Для запуска всех тестов: `pytest`
2. Для запуска unit-тестов и компонетных тестов: `pytest tests/unit/`
3. Для запуска интеграционных: `pytest tests/integration/`

### Проект находится на стадии разработки

**Ведется работа по направлениям:**
- реализация микросервиса для работы с аналитикой;
- подключение алертинга с помощью Grafana;
- замена брокера сообщений (RabbitMQ на Kafka).
