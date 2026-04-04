from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Profile, Message


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Message)
def notify_new_message(sender, instance, created, **kwargs):
    """
    Sinyal untuk mengirim notifikasi real-time via WebSocket saat pesan baru masuk.
    Merender snippet HTML kustom agar bisa langsung diparkir di Inbox dashboard.
    """
    if created:
        channel_layer = get_channel_layer()

        # Render snippet HTML kartu pesan untuk Dashboard Inbox
        # Gunakan render_to_string agar kita bisa kirim HTML siap pakai via socket
        message_html = render_to_string(
            "main/partials/message_card.html", {"msg": instance}
        )

        # Kirim siaran (Broadcasting) ke grup khusus milik Penerima
        async_to_sync(channel_layer.group_send)(
            f"user_dashboard_{instance.recipient.id}",
            {"type": "new_message", "message": message_html},
        )
