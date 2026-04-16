"""
Development settings — use SQLite by default for easy local setup.
Switch USE_MYSQL=true in .env when your MySQL server is ready.
"""

import os

from .base import *  # noqa: F403, F405

DEBUG = True

USE_MYSQL = os.getenv("USE_MYSQL", "False").lower() == "true"

if not USE_MYSQL:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
        }
    }

# Email backend for development (console)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
