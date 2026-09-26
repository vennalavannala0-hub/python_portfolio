"""Production settings for Render (PostgreSQL, WhiteNoise, HTTPS)."""

from .base import *  # noqa: F403
from .env import env_bool, env_list, env_str

DEBUG = env_bool("DEBUG", False)
SECRET_KEY = env_str("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in production.")

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", [".onrender.com"])
if not ALLOWED_HOSTS:
    raise ValueError("ALLOWED_HOSTS must be set in production.")

CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS", ["https://*.onrender.com"])

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = int(env_str("SECURE_HSTS_SECONDS", "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# Render terminates TLS at the proxy. Honor the forwarded protocol.
USE_X_FORWARDED_HOST = True

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

engine = DATABASES["default"].get("ENGINE", "")
if env_bool("DATABASE_SSL_REQUIRE", True) and "postgresql" in engine:
    DATABASES["default"].setdefault("OPTIONS", {})
    DATABASES["default"]["OPTIONS"].setdefault("sslmode", "require")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
