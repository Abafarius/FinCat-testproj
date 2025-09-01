# ---------- Runtime ----------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# утилиты для ожидания БД и pg-библиотека
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd libpq5 \
    && rm -rf /var/lib/apt/lists/*

# 1) зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) исходники проекта
COPY . .

# (не критично, но полезно; завернём в || true)
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

# ждём Postgres, миграции и стартуем gunicorn
CMD sh -c "until nc -z db 5432; do echo '⏳ Waiting for Postgres...'; sleep 1; done; \
           python manage.py migrate && \
           gunicorn core.wsgi:application --bind 0.0.0.0:8000"
