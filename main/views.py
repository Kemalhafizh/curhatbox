from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone

from .models import Message, BlockList
from .forms import ProfileForm, ReplyForm
from .utils import sensor_kata, verify_recaptcha

# --- PUBLIC VIEWS ---

def index(request):
    return render(request, 'main/index.html')

def about_page(request):
    return render(request, 'main/about.html')

def rules_page(request):
    return render(request, 'main/rules.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Selamat datang! Akun berhasil dibuat.")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'main/register.html', {'form': form})

from django_ratelimit.decorators import ratelimit
from django.core.exceptions import PermissionDenied

@ratelimit(key='ip', rate='3/m', method='POST', block=True)
def public_profile(request, slug):
    receiver = get_object_or_404(User, profile__slug=slug)
    
    # Menampilkan pesan publik (yang sudah dibalas)
    public_messages = Message.objects.filter(recipient=receiver, is_public=True)

    if request.method == 'POST':
        content = request.POST.get('pesan')
        client_ip = request.META.get('REMOTE_ADDR')

        # 1. Cek Token reCAPTCHA v3
        recaptcha_token = request.POST.get('g-recaptcha-response')
        if not verify_recaptcha(recaptcha_token):
            messages.error(request, "Gagal mengirim pesan. Sistem mendeteksi aktivitas mencurigakan (Bot).")
            return redirect('public_profile', slug=slug)

        # 2. Cek Block List
        is_blocked = BlockList.objects.filter(user=receiver, ip_address=client_ip).exists()
        if is_blocked:
            messages.error(request, "Akses ditolak. Anda tidak dapat mengirim pesan ke pengguna ini.")
            return redirect('public_profile', slug=slug)

        # 3. Simpan Pesan Lengkap
        if content:
            clean_content = sensor_kata(content)
            Message.objects.create(
                recipient=receiver,
                content=clean_content,
                sender_ip=client_ip
            )
            messages.success(request, "Pesan rahasia terkirim!")
            return redirect('public_profile', slug=slug)

    context = {
        'target_user': receiver,
        'public_messages': public_messages
    }
    return render(request, 'main/profile_public.html', context)


# --- AUTHENTICATED VIEWS ---

@login_required
def dashboard(request):
    inbox = Message.objects.filter(recipient=request.user).select_related('recipient')
    return render(request, 'main/dashboard.html', {'messages': inbox})

@login_required
def reply_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id, recipient=request.user)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=msg)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.replied_at = timezone.now()
            reply.is_public = True
            reply.is_read = True
            reply.save()
            messages.success(request, "Balasan terkirim.")
            
    return redirect('dashboard')

@login_required
def delete_message(request, message_id):
    if request.method == 'POST':
        msg = get_object_or_404(Message, id=message_id, recipient=request.user)
        msg.delete()
        messages.success(request, "Pesan dihapus.")
    return redirect('dashboard')

@login_required
def block_sender(request, message_id):
    msg = get_object_or_404(Message, id=message_id, recipient=request.user)
    
    if msg.sender_ip:
        BlockList.objects.get_or_create(user=request.user, ip_address=msg.sender_ip)
        messages.warning(request, "Pengirim telah diblokir.")
    else:
        messages.error(request, "Gagal memblokir: IP tidak ditemukan.")
        
    return redirect('dashboard')

@login_required
def toggle_favorite(request, message_id):
    msg = get_object_or_404(Message, id=message_id, recipient=request.user)
    msg.is_favorite = not msg.is_favorite
    msg.save()
    status = "dipin" if msg.is_favorite else "dilepas"
    messages.success(request, f"Pesan berhasil {status}.")
    return redirect('dashboard')

@login_required
def edit_profile(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil diperbarui.")
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
        
    return render(request, 'main/edit_profile.html', {'form': form})

# --- ERROR HANDLERS ---

def ratelimit_error_handler(request, exception=None):
    """
    Menangkap error 403 PermissionDenied yang dilempar oleh @ratelimit.
    Memberikan pesan yang lebih ramah ke user daripada halaman 403 bawaan Django.
    """
    
    # Coba deteksi darimana user berasal untuk di-redirect balik
    # Jika gagal ditebak, kembali ke halaman utama.
    referer = request.META.get('HTTP_REFERER', '/')
    messages.error(request, "Tunggu sebentar! Kamu mengirim pesan terlalu cepat. Silakan coba lagi dalam 1 menit.")
    return redirect(referer)