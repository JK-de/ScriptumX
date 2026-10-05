# syntax=docker/dockerfile:1
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_DEBUG=1 \
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0 \
    DJANGO_DB_PATH=/data/db.sqlite3

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libjpeg62-turbo-dev \
        zlib1g-dev \
        libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

RUN mkdir -p /data \
    && chmod +x /app/docker/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["gunicorn", "ScriptumX.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
