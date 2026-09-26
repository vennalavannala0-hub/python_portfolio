"""Local development settings. SQLite is used unless DATABASE_URL is set."""

from .base import *  # noqa: F403
from .env import env_bool, env_list, env_str

DEBUG = env_bool("DEBUG", True)
SECRET_KEY = env_str("SECRET_KEY", "unsafe-development-key-change-me")
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", ["127.0.0.1", "localhost"])
CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
    ["http://127.0.0.1:8000", "http://localhost:8000"],
)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
