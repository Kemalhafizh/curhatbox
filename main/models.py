from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# --- MODEL 1: PROFILE ---
# Fungsinya: Menyimpan data tambahan user yang tidak ada di tabel bawaan Django.
class Profile(models.Model):
    # OneToOneField: Satu user cuma punya satu profil.
    # on_delete=models.CASCADE: Kalau user dihapus, profil ini ikut terhapus.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Slug: Link unik (contoh: curhatbox.com/kemal).
    # unique=True: Tidak boleh ada dua orang yang link-nya sama.
    slug = models.SlugField(unique=True, blank=True)
    
    # Bio: Deskripsi singkat di halaman profil.
    bio = models.TextField(max_length=500, blank=True, help_text="Tulis sapaan untuk pengunjung profilmu.")
    
    # Timestamp: Mencatat kapan akun dibuat.
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # LOGIC OTOMATIS:
        # Jika slug belum diisi, ambil dari username, ubah jadi huruf kecil & ganti spasi jadi strip.
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Profil: {self.user.username}"


# --- MODEL 2: MESSAGE ---
# Fungsinya: Menyimpan pesan rahasia dari anonim.
class Message(models.Model):
    # Penerima: Si User pemilik akun.
    # related_name='messages': Biar nanti gampang panggilnya (user.messages.all())
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    
    # Isi Pesan
    content = models.TextField(verbose_name="Isi Curhatan")
    
    # Waktu: Kapan pesan dikirim (Otomatis terisi saat dibuat)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Status:
    is_read = models.BooleanField(default=False)    # Sudah dibaca user?
    is_public = models.BooleanField(default=False)  # Ditampilkan di publik (Wall)?

    # Fitur Balasan (Reply):
    # null=True, blank=True: Boleh kosong (karena pas pesan baru masuk, pasti belum dibalas).
    reply_content = models.TextField(blank=True, null=True, verbose_name="Balasan Kamu")
    replied_at = models.DateTimeField(blank=True, null=True)

    # KEAMANAN (Security):
    # Kita simpan IP pengirim untuk keperluan moderasi/blokir.
    sender_ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        # Mengurutkan pesan dari yang paling baru (-) ke yang lama.
        ordering = ['-created_at']

    def __str__(self):
        return f"Pesan untuk {self.recipient.username} | {self.created_at.strftime('%d-%m-%Y %H:%M')}"
    
class BlockList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_ips')
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Mencegah duplikasi: Satu user tidak perlu memblokir IP yang sama 2 kali
        unique_together = ('user', 'ip_address')

    def __str__(self):
        return f"{self.user.username} blocked {self.ip_address}"