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

## 🗂 Структура проекта
```
FinCat-testproj/
 ├── back/              # Backend (Django + DRF)
 │   ├── core/          # Настройки Django
 │   ├── orgs/          # Приложение с моделями организаций
 │   ├── manage.py
 │   ├── requirements.txt
 │   └── Dockerfile
 │
 ├── front/             # Frontend (Nuxt3)
 │   ├── app/           # Исходники фронта
 │   ├── package.json
 │   └── Dockerfile
 │
 ├── docker-compose.yml # Compose для запуска
 ├── .env               # Конфигурация окружения
 └── README.md          # Этот файл
```

---

## 🚀 Запуск проекта

### 1. Запуск через Docker (рекомендуется)
```bash
# В корне проекта
docker-compose up --build
```
Сервисы:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- База данных: PostgreSQL (порт 5432)

### 2. Локальный запуск без Docker

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
- Возможна доработка: экспорт в Excel/CSV, AI-summary карточек банка и др.

---

## 👨‍💻 Автор
Тестовое задание — Galymzhan Yessimbek
