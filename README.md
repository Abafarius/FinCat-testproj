# 📂 FinCat — Каталог финансовых организаций

## 📌 Описание проекта
Внутренний сервис для работы с каталогом финансовых организаций.  
Пользователи могут:
- Просматривать список организаций
- Смотреть детальную карточку организации

Администраторы могут:
- Добавлять, редактировать и удалять организации
- Управлять лицензиями

Авторизация реализована через **JWT-токены**. Доступ разделён по ролям (**admin**, **user**).

---

## ⚙️ Стек технологий
- **Backend:** Python 3.11, Django 5.x, Django REST Framework, SimpleJWT
- **Frontend:** Vue.js 3, Nuxt 3, TypeScript
- **БД:** PostgreSQL (по умолчанию SQLite для локальной разработки)
- **Docker & Docker Compose** для контейнеризации

---

## 🚀 Запуск проекта

## 🚀 Быстрый старт (Docker)

**Требуется:** Docker Desktop.

1. Склонируйте репозиторий и перейдите в **корень проекта** (там, где `docker-compose.yml`).
2. Создайте файл **`.env`** в корне и вставьте:
   ```env
   # --- Postgres ---
   POSTGRES_DB=fincat
   POSTGRES_USER=fincat
   POSTGRES_PASSWORD=fincat

   # --- Django ---
   DJANGO_SECRET_KEY=please-change-me
   DJANGO_ALLOWED_HOSTS=backend,localhost,127.0.0.1
   DJANGO_DEBUG=False
   CORS_ALLOW_ALL_ORIGINS=True
   CSRF_TRUSTED_ORIGINS=http://localhost:3000

   # --- Nuxt (frontend) ---
   NUXT_PUBLIC_API_BASE=http://localhost:8000/api
3. Поднимите контейнеры:
```bash
docker compose up --build
```
4. Создайте суперпользователя (админа):
```bash
docker compose exec backend python manage.py createsuperuser
```
5. (Опционально) Заполните базу демо-данными:
```bash
docker compose exec backend python manage.py seed
```
### Локальный запуск без Docker

#### Backend
```bash
cd back
python -m venv venv
source venv/bin/activate   # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Backend доступен на: http://127.0.0.1:8000

#### Frontend
```bash
cd front/app
npm install
npm run dev
```
Frontend доступен на: http://localhost:3000

---

## 🔑 Авторизация
- Регистрация и вход реализованы через `/api/auth/`
- JWT-токены:
  - `access` — для доступа к API
  - `refresh` — для обновления токена
- Все защищённые эндпоинты требуют заголовка:
  ```
  Authorization: Bearer <access_token>
  ```

---

## 📚 Основные эндпоинты (Backend API)
- `POST /api/auth/register/` — регистрация
- `POST /api/auth/login/` — вход, получение токенов
- `GET /api/orgs/` — список организаций
- `POST /api/orgs/` — создать организацию (admin)
- `GET /api/orgs/{id}/` — получить организацию
- `PUT /api/orgs/{id}/` — редактировать (admin)
- `DELETE /api/orgs/{id}/` — удалить (admin)

---

## 🧩 Дополнительно
- Реализован seed-скрипт для заполнения тестовых данных:
```bash
cd back
python manage.py seed
```

---

## 👨‍💻 Автор
Тестовое задание — Galymzhan Yessimbek
