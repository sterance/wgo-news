"""
Django settings for the WGO News backend.

Configuration that changes between machines (secret key, hosts, allowed
front-end origins) is read from environment variables, with defaults that
work out of the box for local development.
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def env_list(name: str, default: str = "") -> list[str]:
    """Read a comma-separated environment variable into a list."""
    return [item.strip() for item in os.environ.get(name, default).split(",") if item.strip()]


# --- Core -------------------------------------------------------------------

DEBUG = os.environ.get("DJANGO_DEBUG", "true").lower() in {"1", "true", "yes"}

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured("Set DJANGO_SECRET_KEY when DJANGO_DEBUG is off.")
    SECRET_KEY = "dev-only-insecure-key-do-not-use-in-production"

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")

# --- Applications -----------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "rest_framework",
    "corsheaders",
    # Local
    "news",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # must sit above CommonMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --- Database ---------------------------------------------------------------

# Two SQLite files: "default" (auth.db) holds Django's own tables (auth, admin,
# sessions, contenttypes); "news" (news.db) holds the news app's tables.
# DJANGO_DB_DIR overrides the directory they live in.
DB_DIR = Path(os.environ.get("DJANGO_DB_DIR", BASE_DIR))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(DB_DIR / "auth.db"),
    },
    "news": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(DB_DIR / "news.db"),
    },
}

DATABASE_ROUTERS = ["config.db_router.NewsRouter"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Auth / i18n ------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-au"
TIME_ZONE = "Australia/Melbourne"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# The React app built for Django to serve (`npm run build:django`). Only added
# when it exists, so a checkout without it (e.g. the Docker build) still works.
# Restart runserver after the first build so the directory is picked up.
FRONTEND_BUILD_DIR = BASE_DIR / "frontend_build"
STATICFILES_DIRS = [FRONTEND_BUILD_DIR] if FRONTEND_BUILD_DIR.is_dir() else []

# Anything that needs a login (the React /admin page) sends people to the
# Django admin's login page.
LOGIN_URL = "/django-admin/login/"

# --- REST framework ---------------------------------------------------------

REST_FRAMEWORK = {
    # Reads are public. Writes need a superuser logged in through the Django
    # admin; the session cookie authenticates them and CSRF protects them.
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.SessionAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["news.permissions.IsSuperuserOrReadOnly"],
    "DEFAULT_PAGINATION_CLASS": None,
}

# --- CORS (React front end) -------------------------------------------------
# Only the API is exposed cross-origin, and only for reads: no credentials are
# allowed, so admin writes only work same-origin (Vite proxy or Django-served). Add your deployed front-end URL, e.g.
#   DJANGO_CORS_ORIGINS=https://wgo-news.pages.dev

CORS_ALLOWED_ORIGINS = env_list(
    "DJANGO_CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173,http://127.0.0.1:4173",
)
CORS_URLS_REGEX = r"^/api/.*$"
