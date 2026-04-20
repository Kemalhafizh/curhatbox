from .settings import *

# Override DATABASES untuk pengujian agar menggunakan SQLite di memory (Sangat Cepat & Terisolasi)
# Ini mencegah masalah "Permission Denied" pada PostgreSQL Production.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Menggunakan Local Memory Cache saat testing untuk mendukung pengujian django-ratelimit
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Paksa Celery agar berjalan Synchronous secara In-Memory selama testing
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_STORE_EAGER_RESULT = True
