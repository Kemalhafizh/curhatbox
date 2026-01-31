from django.contrib import admin
from .models import Profile, Message

# 1. Modifikasi tampilan Tabel Pesan (IP Pengirim terlihat)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):  # <--- INI YANG SAYA PERBAIKI
    # Kolom yang muncul di daftar
    list_display = ('penerima_pesan', 'cuplikan_pesan', 'sender_ip', 'created_at', 'is_read')
    
    # Filter samping
    list_filter = ('recipient', 'created_at', 'is_read')
    
    # Pencarian (Search)
    search_fields = ('content', 'sender_ip', 'recipient__username')
    
    # Read-only
    readonly_fields = ('sender_ip', 'created_at')

    # Custom column title
    def penerima_pesan(self, obj):
        return obj.recipient.username
    penerima_pesan.short_description = 'Penerima'

    def cuplikan_pesan(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    cuplikan_pesan.short_description = 'Isi Pesan'

# 2. Daftarkan Profile
admin.site.register(Profile)