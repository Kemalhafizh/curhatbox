import os
from celery import Celery

# Set konfigurasi default Django untuk program command-line Celery.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "curhatbox.settings")

app = Celery("curhatbox")

# Pake string agar *worker* Celery ga perlu secara paksa serialisasi
# (pickle) objek konfigurasi karena kita aturnya di namespace CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Cari semua file tasks.py di dalam semua aplikasi yang ada di INSTALLED_APPS otomatis.
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Celery Request: {self.request!r}')
