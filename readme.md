# Flask Testcase Project

## ТЗ
- [Техническое задание (ТЗ)](TECHNICAL_REQUIREMENTS.md)

## Описание
Проект включает в себя:
- **Админка** с управлением пользователями и транзакциями.
- **Celery задачи** для проверки статусов транзакций и баланса USDT-кошельков.
- **Swagger-документация** для API.
- **PostgreSQL** как основная база данных.
- **Redis** как брокер для Celery.

---

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/Sleeeepy7/flask_testcase.git
cd flask-testcase
```

### 2. Настройка переменных окружения
Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```

Отредактируйте `.env` при необходимости. Пример:
```env
# PostgreSQL настройки
PG_USER=postgres
PG_PASSWORD=your_password
PG_DB=flask_test
PG_HOST=db # не менять

# Redis настройки
REDIS_HOST=redis # не менять
REDIS_PORT=6379
REDIS_DB=0
REDIS__URL=redis://redis:6379/0
```

### 3. Запуск контейнеров
Для запуска приложения выполните:
```bash
docker-compose up --build
```

После успешного запуска:
- Приложение доступно на `http://127.0.0.1:5000`.
- Документация доступна по адресу `http://127.0.0.1:5000/apidocs`.

---

## Основные команды

### Запуск проекта
```bash
docker-compose up --build
```

### Остановка проекта
```bash
docker-compose down
```

### Удаление данных (очистка контейнеров и томов)
```bash
docker-compose down -v
```

### Пример выполнения миграций вручную (первая выполняется сама через entrypoint)
```bash
docker-compose exec web alembic revision --autogenerate -m "Your migration name"
docker-compose exec web alembic upgrade head
```

---

## Тестовые данные
1. **Админка** доступна по адресу `http://127.0.0.1:5000/admin`.
2. Создайте пользователей и транзакции через админ-панель.

---
