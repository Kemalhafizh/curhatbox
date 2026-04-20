# Import app Celery agar langsung dimuat saat layanan Django/Daphne dihidupkan.
from .celery import app as celery_app

__all__ = ("celery_app",)
