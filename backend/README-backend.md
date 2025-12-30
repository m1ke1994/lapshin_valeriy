# Backend (Django + DRF)

Backend расположен в `backend/` и предоставляет API/CMS для главной страницы, проектов и сертификатов.

## Быстрый старт
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env     # при необходимости
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

## Настройки окружения
- `SECRET_KEY` — секрет Django.
- `DEBUG` — включает debug-режим.
- `ALLOWED_HOSTS` — через запятую.
- `CORS_ALLOWED_ORIGINS` — URL фронтенда (по умолчанию: localhost:3000, localhost:5173, https://website-ikb.vercel.app).
- `DATABASE_URL` — поддерживает SQLite/PostgreSQL (см. dj-database-url).
- `MEDIA_URL` / `MEDIA_ROOT` — откуда отдавать загруженные файлы.

## Основные команды
- `python manage.py migrate`
- `python manage.py createsuperuser`
- `python manage.py runserver`

## Маршруты
- `GET /api/public/home/` — агрегированное содержимое главной (секции + активные проекты/сертификаты).
- `GET|POST /api/projects/`, `GET|PATCH|DELETE /api/projects/{id}/`
- `GET|POST /api/certificates/`, `GET|PATCH|DELETE /api/certificates/{id}/`
- `GET|POST /api/content/` — блоки контента (key/locale/title/body/extra).
- `POST /api/auth/token` + `POST /api/auth/refresh` — JWT.
- `GET /api/docs/` — Swagger (drf-spectacular).

Публичное чтение разрешено, изменения доступны после JWT-аутентификации или через Django Admin (`/admin/`).

## Медиа
Файлы загружаются в `MEDIA_ROOT` (по умолчанию `backend/media`). В DEV файлы отдаёт Django (`MEDIA_URL`).

## Подключение фронта
В Nuxt выставьте `NUXT_PUBLIC_API_BASE_URL` (см. `.env.example` в корне) и обращайтесь к API, например:
- `/api/public/home?locale=ru`
- `/api/projects/?locale=ru`
- `/api/certificates/?locale=ru`
