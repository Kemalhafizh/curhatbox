from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_email_task(subject, body, from_email, to_emails, html_message=None):
    """
    Tugas Celery Asinkron untuk melempar pekerjaan pengiriman email
    ke background proses (Pabrik Belakang).
    """
    try:
        email = EmailMultiAlternatives(subject, body, from_email, to_emails)
        if html_message:
            email.attach_alternative(html_message, "text/html")
        email.send()
        logger.info(f"Berhasil mengirim email asinkron ke {to_emails}")
        return True
    except Exception as e:
        logger.error(f"Gagal mengirim email Celery ke {to_emails}: {e}")
        return False

@shared_task
def cleanup_disposable_messages():
    """
    Membersihkan pesan 'Bom Waktu' (Disposable) yang:
    1. Sudah dibaca.
    2. Atau usianya sudah lebih dari 24 jam meskipun belum dibaca.
    """
    from main.models import Message
    
    # Kriteria 1: Pesan sekali baca yang sudah dibaca
    query_read = Message.objects.filter(is_disposable=True, is_read=True)
    count_read = query_read.count()
    query_read.delete()
    
    # Kriteria 2: Basi lebih dari 24 jam
    yesterday = timezone.now() - timedelta(hours=24)
    query_expired = Message.objects.filter(is_disposable=True, created_at__lte=yesterday)
    count_expired = query_expired.count()
    query_expired.delete()
    
    total = count_read + count_expired
    if total > 0:
        logger.info(f"Celery Beat: Berhasil membuang {total} pesan bom waktu kadaluwarsa.")
    return total
