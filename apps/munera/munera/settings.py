import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from django.utils.translation import gettext_lazy as _


BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = Path(os.environ.get("MUNERA_INSTANCE_DIR", BASE_DIR / "instance"))

DEBUG = os.environ.get("MUNERA_DEBUG", "1") == "1"

if DEBUG:
    SECRET_KEY = "django-insecure-orlb%-uoh4@7*9a68)oz_mam1%-%u_$g=8o)xokkl%*e8mxr7v"
    INSTANCE_DIR.mkdir(exist_ok=True)
else:
    SECRET_KEY = os.environ.get("MUNERA_SECRET_KEY", get_random_secret_key)
    if hosts := os.getenv("MUNERA_ALLOWED_HOSTS"):
        ALLOWED_HOSTS = hosts.split(",")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "widget_tweaks",
    "munera",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "munera.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "munera.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": INSTANCE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
    },
}

LANGUAGE_CODE = "nl-nl"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

LANGUAGES = (
    ("nl", _("Dutch")),
    ("en", _("English")),
)

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = (BASE_DIR / "assets",)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "munera.User"

MUNERA_LOGBOEK_ENDPOINT = os.environ.get("MUNERA_LOGBOEK_ENDPOINT", "127.0.0.1:9000")
MUNERA_CURRUS_URL = os.environ.get("MUNERA_CURRUS_URL", "http://127.0.0.1:8081")
