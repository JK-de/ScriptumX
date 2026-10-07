"""
Django settings for ScriptumX project.
"""

from os import path
import os
import warnings

PROJECT_ROOT = path.dirname(path.abspath(path.dirname(__file__))).replace('\\', '/')

DEBUG = os.environ.get('DJANGO_DEBUG', '1') == '1'

ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0').split(',')
    if h.strip()
]

ADMINS = (
    ('admin', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get(
            'DJANGO_DB_PATH',
            path.join(PROJECT_ROOT, 'db.sqlite3'),
        ),
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            path.join(PROJECT_ROOT, 'X/templates'),
            path.join(PROJECT_ROOT, 'web/templates'),
        ],
        'OPTIONS': {
            'builtins': [
                'X.templatetags.legacy',
            ],
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'X.context_processors.ux_chrome',
            ],
        },
    },
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Mail via msmtp/sendmail; logs reset links when relay is not configured.
EMAIL_BACKEND = os.environ.get(
    'DJANGO_EMAIL_BACKEND',
    'ScriptumX.mail.MsmtpEmailBackend',
)
DEFAULT_FROM_EMAIL = os.environ.get(
    'DJANGO_DEFAULT_FROM_EMAIL',
    'scriptumx@localhost',
)
SERVER_EMAIL = DEFAULT_FROM_EMAIL

TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'de'
LANGUAGES = (
    ('de', 'Deutsch'),
    ('en', 'English'),
)
LOCALE_PATHS = (
    path.join(PROJECT_ROOT, 'locale'),
)
SITE_ID = 1
USE_I18N = True
USE_TZ = True

MEDIA_ROOT = ''
MEDIA_URL = ''

STATIC_ROOT = path.join(PROJECT_ROOT, 'static').replace('\\', '/')
STATIC_URL = '/static/'

STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

_default_secret = 'dev-only-change-me-n(bd1f1c%e8=_xad02x5qtfn%wgwpi492e$8_erx+d)!tpeoim'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', _default_secret)
if not DEBUG and SECRET_KEY == _default_secret:
    raise ValueError(
        'DJANGO_SECRET_KEY must be set to a strong value when DJANGO_DEBUG=0'
    )

# Comma-separated origins for CSRF when behind Traefik/Caddy/nginx, e.g.
# https://scriptumx.example.com,https://www.example.com
CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',')
    if o.strip()
]

# Trust X-Forwarded-Proto / Host from a reverse proxy terminating TLS (Caddy/nginx).
if os.environ.get('DJANGO_BEHIND_PROXY', '0') == '1' or not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = os.environ.get('DJANGO_USE_X_FORWARDED_HOST', '1') == '1'

if not DEBUG or os.environ.get('DJANGO_BEHIND_PROXY', '0') == '1':
    SESSION_COOKIE_SECURE = os.environ.get('DJANGO_SESSION_COOKIE_SECURE', '1') == '1'
    CSRF_COOKIE_SECURE = os.environ.get('DJANGO_CSRF_COOKIE_SECURE', '1') == '1'

if not DEBUG:
    SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', '0') == '1'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'X.access_middleware.ProjectAccessMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'scriptumx.mail': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

# django-htmlmin is unmaintained; off by default. Enable only via env
# (and with the optional package from requirements-dev.txt / requirements.txt extras).
HTML_MINIFY = os.environ.get('DJANGO_HTML_MINIFY', '0') == '1'
if HTML_MINIFY:
    try:
        import htmlmin  # noqa: F401
    except ImportError:
        warnings.warn(
            'DJANGO_HTML_MINIFY=1 but django-htmlmin is not installed; minify disabled',
            RuntimeWarning,
        )
        HTML_MINIFY = False
    else:
        MIDDLEWARE.insert(2, 'htmlmin.middleware.HtmlMinifyMiddleware')
        MIDDLEWARE.insert(3, 'htmlmin.middleware.MarkRequestMiddleware')

ROOT_URLCONF = 'ScriptumX.urls'
WSGI_APPLICATION = 'ScriptumX.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'ScriptumX',
    'X',
    'web',
    'authentication',
    'report',
    'crispy_forms',
    'crispy_bootstrap3',
    'colorfield',
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap3'
CRISPY_TEMPLATE_PACK = 'bootstrap3'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}
