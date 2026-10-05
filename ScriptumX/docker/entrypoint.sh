#!/bin/sh
set -e

cd /app

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Bootstrap superuser only in explicit cases:
# - DJANGO_DEBUG=1 (local/dev compose), or
# - DJANGO_ALLOW_BOOTSTRAP_SUPERUSER=1 (opt-in for shared envs)
# Never create the known-insecure admin/admin pair when DEBUG is off.
bootstrap_allowed=0
if [ "${DJANGO_DEBUG:-0}" = "1" ]; then
  bootstrap_allowed=1
elif [ "${DJANGO_ALLOW_BOOTSTRAP_SUPERUSER:-0}" = "1" ]; then
  bootstrap_allowed=1
fi

if [ "$bootstrap_allowed" = "1" ] \
  && [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] \
  && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
  if [ "${DJANGO_DEBUG:-0}" != "1" ] \
    && [ "${DJANGO_SUPERUSER_USERNAME}" = "admin" ] \
    && [ "${DJANGO_SUPERUSER_PASSWORD}" = "admin" ]; then
    echo "Refusing to bootstrap insecure admin/admin when DJANGO_DEBUG!=1" >&2
    exit 1
  fi
  python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ["DJANGO_SUPERUSER_USERNAME"]
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
password = os.environ["DJANGO_SUPERUSER_PASSWORD"]
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Created superuser '{username}'")
else:
    print(f"Superuser '{username}' already exists")
PY
elif [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] || [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
  echo "Skipping superuser bootstrap (set DJANGO_DEBUG=1 or DJANGO_ALLOW_BOOTSTRAP_SUPERUSER=1)" >&2
fi

exec "$@"
