from .settings import *  # noqa

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mailhog"
EMAIL_PORT = 1025

CELERY_DEFAULT_QUEUE = "genesis-dev"
