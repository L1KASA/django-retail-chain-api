# django-retail-chain-api

Веб-приложение для управления сетью по продаже электроники.

## Стек

- Python 3.10+
- Django 4.2+
- Django REST Framework
- PostgreSQL 15
- Docker, Docker Compose
- Celery, Redis

## Установка и запуск
### 1. Клонировать репозиторий

```bash
git clone <url>
cd django-retail-chain-api
```

### 2. Создать .env файл

```bash
cp .env.example .env
```

### 3. Запустить контейнеры

```bash
docker compose up -d
```
### 4. Применить миграции

```bash
docker compose exec web python manage.py migrate
```
### 5. Создать суперпользователя

```bash
docker compose exec web python manage.py createsuperuser
```

## Миграции
### Создать новые миграции

```bash
docker compose exec web python manage.py makemigrations
```
### Применить миграции

```bash
docker compose exec web python manage.py migrate
```
### Откатить миграции

```bash
# Пример откатывания последней миграции приложения
docker compose exec web python manage.py migrate retail <номер_предыдущей_миграции>

# Откатить все миграции приложения
docker compose exec web python manage.py migrate retail zero
```
## Посев данных

```bash
docker compose exec web python manage.py seed_data
```

## API
http://localhost:8000/api/v1/

## Админ-панель
http://localhost:8000/admin/