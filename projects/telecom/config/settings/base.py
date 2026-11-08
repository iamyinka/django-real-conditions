"""Settings shared by every environment.

Environment-specific modules (dev.py, test.py, and later prod.py) import
everything from here and override only what differs. Secrets and
per-deployment values come from environment variables, never from this file.
"""

from pathlib import Path

from config.env import env, env_bool, env_list

# projects/telecom/ : three levels up from config/settings/base.py
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Required: startup fails with ImproperlyConfigured if it's missing.
# The key that startproject generated was removed, because a committed key isn't a secret.
SECRET_KEY = env("DJANGO_SECRET_KEY")

# Secure by default: an environment has to opt in to debug mode explicitly.
DEBUG = env_bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", [])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Project apps
    "core",
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

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "config.wsgi.application"

# PostgreSQL in its own container. DB_HOST is the *Compose service name* ("db"):
# Compose runs a DNS server on the project network that resolves service names
# to container IPs. "localhost" inside the web container is the web container itself.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT", "5432"),
        # Fail fast. Without this, connecting to an unreachable host can block for minutes,
        # and so would /readyz and every request.
        "OPTIONS": {"connect_timeout": 5},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"  # store and compute in UTC; convert to local time only for display
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

# New in Django 6.1: named mail configurations. Console backend = print emails to stdout.
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}
