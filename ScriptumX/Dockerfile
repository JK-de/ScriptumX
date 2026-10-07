# syntax=docker/dockerfile:1
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_DEBUG=0 \
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0 \
    DJANGO_DB_PATH=/data/db.sqlite3

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gettext \
        libjpeg62-turbo-dev \
        zlib1g-dev \
        libfreetype6-dev \
        msmtp \
        msmtp-mta \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system --gid 1000 app \
    && useradd --system --uid 1000 --gid app --home /app --shell /usr/sbin/nologin app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

# compilemessages loads Django settings; Dockerfile ENV has DJANGO_DEBUG=0,
# which requires a non-default SECRET_KEY (runtime compose sets the real one).
RUN mkdir -p /data /app/static \
    && chmod +x /app/docker/entrypoint.sh \
    && DJANGO_SECRET_KEY=docker-build-compilemessages \
        python manage.py compilemessages \
    && chown -R app:app /app /data

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=5)"

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["gunicorn", "ScriptumX.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
