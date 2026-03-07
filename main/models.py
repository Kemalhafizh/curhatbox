from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# --- MODEL 1: PROFILE ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    slug = models.SlugField(unique=True, blank=True)
    
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, help_text="Upload foto profilmu.")
    theme_color = models.CharField(max_length=7, default='#f8f9fa', help_text="Warna tema profil (Hex Code)")

    bio = models.TextField(max_length=500, blank=True, help_text="Tulis sapaan untuk pengunjung profilmu.")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Profil: {self.user.username}"


# --- MODEL 2: MESSAGE ---
class Message(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    
    content = models.TextField(verbose_name="Isi Curhatan")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_read = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)

    reply_content = models.TextField(blank=True, null=True, verbose_name="Balasan Kamu")
    replied_at = models.DateTimeField(blank=True, null=True)

    sender_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # --- Self Destruct ---
    is_disposable = models.BooleanField(default=False, verbose_name="Pesan Sekali Baca")
    
    # --- Hint Pengirim (Device Tracking) ---
    sender_device = models.CharField(max_length=50, blank=True, null=True, help_text="Sistem Operasi (Contoh: Android, iOS, Windows)")
    sender_browser = models.CharField(max_length=50, blank=True, null=True, help_text="Browser (Contoh: Chrome, Safari)")
    
    # --- Quick Reactions ---
    reaction = models.CharField(max_length=10, blank=True, null=True, verbose_name="Reaksi Cepat")

    class Meta:
        ordering = ['-is_favorite', '-created_at']

    def __str__(self):
        return f"Pesan untuk {self.recipient.username} | {self.created_at.strftime('%d-%m-%Y %H:%M')}"
    
class BlockList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_ips')
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ip_address')

    def __str__(self):
        return f"{self.user.username} blocked {self.ip_address}"