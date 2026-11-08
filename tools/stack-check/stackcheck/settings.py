import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "stack-check-not-a-secret"
DEBUG = False
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "daphne",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.postgres",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "corsheaders",
    "channels",
    "storages",
    "probe",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csp.ContentSecurityPolicyMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]
ROOT_URLCONF = "stackcheck.urls"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "APP_DIRS": True}]
WSGI_APPLICATION = "stackcheck.wsgi.application"
ASGI_APPLICATION = "stackcheck.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "check",
        "USER": "check",
        "PASSWORD": "check",
        "HOST": os.environ.get("DB_HOST", "db"),
    }
}
USE_TZ = True
TIME_ZONE = "UTC"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
S3 = {
    "bucket_name": "check",
    "endpoint_url": os.environ.get("S3_ENDPOINT", "http://s3:8333"),
    "access_key": "check",
    "secret_key": "check",
    "region_name": "us-east-1",
    "addressing_style": "path",
    # Without this, boto3 1.43 + django-storages 1.14.6 presign with legacy SigV2
    # (AWSAccessKeyId=...&Signature=...). Some providers reject SigV2 outright.
    "signature_version": "s3v4",
}
STORAGES = {
    "default": {"BACKEND": "storages.backends.s3.S3Storage", "OPTIONS": S3},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 2,
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
}
CORS_ALLOWED_ORIGINS = ["https://app.example.com"]

from django.utils.csp import CSP  # noqa: E402

SECURE_CSP = {"default-src": [CSP.SELF]}

BROKER = os.environ.get("BROKER_URL", "redis://redis:6379")
CELERY_BROKER_URL = BROKER + "/0"
CELERY_RESULT_BACKEND = BROKER + "/1"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [BROKER + "/2"]},
    }
}
TASKS = {"default": {"BACKEND": "django.tasks.backends.immediate.ImmediateBackend"}}
