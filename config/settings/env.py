"""Small helpers for reading environment variables."""

import os


def env_str(name, default=""):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip()


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name, default=None):
    value = os.environ.get(name)
    if not value:
        return list(default or [])
    return [item.strip() for item in value.split(",") if item.strip()]
