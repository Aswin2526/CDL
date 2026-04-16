"""
Production settings — enable when deploying ChitraBazar.
"""

from .base import *  # noqa: F403, F405

DEBUG = False

# Security settings (uncomment and tune for deployment)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
