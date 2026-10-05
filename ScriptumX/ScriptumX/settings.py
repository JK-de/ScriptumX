"""
Django settings for ScriptumX project.
"""

from os import path
import os

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
            ],
        },
    },
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'de-de'
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

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'dev-only-change-me-n(bd1f1c%e8=_xad02x5qtfn%wgwpi492e$8_erx+d)!tpeoim',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap3'
CRISPY_TEMPLATE_PACK = 'bootstrap3'

HTML_MINIFY = True

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}
