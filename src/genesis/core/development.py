from .settings import *  # noqa

DEBUG = True

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static_files")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
