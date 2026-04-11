import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models.functions import ExtractHour, TruncDate
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.translation import gettext as _

# Third-party imports
from django_ratelimit.decorators import ratelimit
from user_agents import parse

# Local app imports
from .forms import ProfileForm, ReplyForm, CustomUserCreationForm
from .models import BlockList, Message, QnASession
from .utils import sensor_kata, verify_recaptcha

# Daftar emoji lengkap yang anti terpecah (hindari pemecahan byte Unicode di Template HTML)
QUICK_REACTIONS = [
    "🔥",
    "❤️",
    "💀",
    "🤡",
    "😄",
    "😂",
    "😭",
    "🥺",
    "😡",
    "🤯",
    "🤮",
    "🤫",
    "👍",
    "👎",
    "✨",
    "🙏",
    "👀",
    "💯",
]

# ==============================================================================
# PUBLIC VIEWS (Akses Tanpa Login)
# ==============================================================================


def index(request):
    """
    Menampilkan halaman utama (Landing Page).
    
    Halaman ini merupakan pintu masuk utama bagi pengunjung non-login.
    """
    return render(request, "main/index.html")


def about_page(request):
    """Menampilkan halaman Tentang Kami."""
    return render(request, "main/about.html")


def faq_page(request):
    """Menampilkan halaman Pusat Bantuan/FAQ."""
    return render(request, "main/faq.html")


def rules_page(request):
    """Menampilkan halaman Aturan Main/Kebijakan."""
    return render(request, "main/rules.html")


def register(request):
    """
    Menangani pendaftaran pengguna baru.
    
    Mengarahkan pengguna ke dashboard jika sudah login. Validasi form
    pendaftaran dilakukan secara server-side dengan reCAPTCHA di backend (opsional).
    """
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _("Selamat datang! Akun berhasil dibuat."))
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()

    return render(request, "main/register.html", {"form": form})


# --- PASSWORD RESET CUSTOMIZATIONS (dengan Fitur Resend & Cooldown) ---

class CustomPasswordResetView(PasswordResetView):
    """
    Subclass PasswordResetView untuk menangani alur reset password secara kustom.
    
    Menyimpan email ke session agar dapat digunakan kembali oleh fitur 'Resend Email'
    tanpa meminta pengguna memasukkan email berulang kali.
    """
    def form_valid(self, form):
        # Simpan email ke session untuk fitur resend
        self.request.session['password_reset_email'] = form.cleaned_data['email']
        return super().form_valid(form)


def resend_password_reset_email(request):
    """
    View untuk menangani pengiriman ulang email reset password
    dengan pembatasan cooldown 60 detik via Redis.
    """
    email = request.session.get('password_reset_email')
    
    if not email:
        messages.error(request, _("Sesi berakhir. Silakan masukkan email Anda kembali."))
        return redirect('password_reset')

    # Cek Cooldown di Cache (Redis)
    cache_key = f"password_reset_resend_cooldown_{email}"
    cooldown = cache.get(cache_key)
    
    if cooldown:
        messages.warning(request, _("Mohon tunggu sebentar sebelum mengirim ulang email."))
        return redirect('password_reset_done')

    from main.forms import AsyncPasswordResetForm
    
    # Trigger pengiriman email menggunakan form Asinkron Celery
    form = AsyncPasswordResetForm(data={'email': email})
    if form.is_valid():
        form.save(
            request=request,
            email_template_name="registration/password_reset_email.txt",
            html_email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            from_email=settings.DEFAULT_FROM_EMAIL,
        )
        # Set Cooldown selama 60 detik
        cache.set(cache_key, True, 60)
        messages.success(request, _("Email baru telah dikirimkan ke kotak masuk Anda."))
    else:
        messages.error(request, _("Gagal mengirim ulang email. Pastikan format email benar."))

    return redirect('password_reset_done')


@login_required
def trigger_reset_for_current_user(request):
    """
    Memungkinkan user yang login untuk langsung mengirim link reset 
    ke email terdaftar mereka jika lupa password lama.
    """
    email = request.user.email
    if not email:
        messages.error(request, _("Akun Anda tidak memiliki email yang terdaftar."))
        return redirect('edit_profile')

    # Gunakan logika resend yang sudah ada dengan menset session email
    request.session['password_reset_email'] = email
    return resend_password_reset_email(request)


@ratelimit(key="ip", rate="3/m", method="POST", block=True)
def public_profile(request, slug, qna_slug=None):
    """
    Menampilkan profil publik pengguna dan memproses pengiriman pesan anonim.
    
    Dilengkapi dengan fitur:
    - Proteksi Rate Limit (3 pesan per menit per IP).
    - Verifikasi reCAPTCHA v3 untuk mencegah bot.
    - Filter kata sensor (bad words filtering).
    - Dukungan sesi QnA spesifik.
    """
    receiver = get_object_or_404(User, profile__slug=slug)
    public_messages = Message.objects.filter(recipient=receiver, is_public=True)
    
    qna_session = None
    if qna_slug:
        qna_session = get_object_or_404(QnASession, user=receiver, slug=qna_slug)
        if not qna_session.is_active:
            messages.warning(request, _("Sesi QnA / Pertanyaan ini sudah ditutup oleh pengguna."))
            return redirect("public_profile", slug=slug)


    if request.method == "POST":
        content = request.POST.get("pesan")

        # --- IP SPOOFING FIX: Dukungan Reverse Proxy ---
        # Tarik IP Asli pengunjung yang diteruskan Nginx, fallback ke localhost jika akses langsung
        client_ip = request.META.get("HTTP_X_REAL_IP", request.META.get("REMOTE_ADDR"))

        # Parse User-Agent untuk Device Tracking
        ua_string = request.META.get("HTTP_USER_AGENT", "")
        user_agent = parse(ua_string)
        device_os = user_agent.os.family
        browser = user_agent.browser.family

        # 1. Validasi Token reCAPTCHA v3
        recaptcha_token = request.POST.get("g-recaptcha-response")
        if not verify_recaptcha(recaptcha_token):
            messages.error(
                request,
                _(
                    "Gagal mengirim pesan. Sistem mendeteksi aktivitas mencurigakan (Bot)."
                ),
            )
            return redirect("public_profile", slug=slug)

        # 2. Validasi Daftar Blokir (Block List)
        is_blocked = BlockList.objects.filter(
            user=receiver, ip_address=client_ip
        ).exists()
        if is_blocked:
            messages.error(
                request,
                _("Akses ditolak. Anda tidak dapat mengirim pesan ke pengguna ini."),
            )
            return redirect("public_profile", slug=slug)

        # 3. Proses Penyimpanan Pesan
        if content:
            clean_content = sensor_kata(content)
            is_disposable = request.POST.get("is_disposable") == "on"

            new_msg = Message.objects.create(
                recipient=receiver,
                content=clean_content,
                sender_ip=client_ip,
                sender_device=device_os,
                sender_browser=browser,
                is_disposable=is_disposable,
                qna_session=qna_session,
            )

            # --- BROADCAST WEBSOCKET (REAL-TIME) ---
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync
            from django.template.loader import render_to_string

            channel_layer = get_channel_layer()
            html_content = render_to_string(
                "main/partials/message_card.html",
                {"msg": new_msg, "quick_reactions": QUICK_REACTIONS, "user": receiver},
                request=request,
            )
            async_to_sync(channel_layer.group_send)(
                f"user_dashboard_{receiver.id}",
                {"type": "new_message", "message": html_content},
            )

            messages.success(request, _("Pesan rahasiamu terkirim! 🚀"))
            return redirect("public_profile", slug=slug)

    context = {
        "target_user": receiver,
        "public_messages": public_messages,
        "recaptcha_site_key": getattr(settings, "RECAPTCHA_PUBLIC_KEY", ""),
        "qna_session": qna_session,
    }
    return render(request, "main/profile_public.html", context)


# ==============================================================================
# AUTHENTICATED VIEWS (Wajib Login)
# ==============================================================================


@login_required
def dashboard(request):
    """
    Menampilkan halaman Dashboard (Kotak Masuk) utama pengguna.
    
    Menangani:
    - Filter pesan berdasarkan sesi QnA.
    - Paginasi daftar pesan (15 pesan per halaman).
    - Notifikasi real-time untuk pesan baru yang belum dibaca.
    - Penandaan status 'read' secara otomatis saat halaman dibuka.
    """
    qna_filter_id = request.GET.get('qna')
    message_qs = Message.objects.filter(recipient=request.user)
    
    if qna_filter_id:
        message_qs = message_qs.filter(qna_session_id=qna_filter_id)

    message_list = (
        message_qs
        .select_related("recipient", "qna_session")
        .order_by("-created_at")
    )
    
    qna_sessions = QnASession.objects.filter(user=request.user).order_by('-created_at')

    # Notifikasi pesan baru
    new_messages_count = message_list.filter(is_read=False).count()
    if new_messages_count > 0:
        messages.info(
            request,
            _("Hore! Kamu memiliki %(count)d pesan rahasia baru yang belum dibaca! ✨")
            % {"count": new_messages_count},
        )

    # Tandai pesan sebagai telah dibaca
    Message.objects.filter(recipient=request.user, is_read=False).update(is_read=True)

    # Setup Paginasi (15 pesan per halaman)
    paginator = Paginator(message_list, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "inbox_messages": message_list,
        "quick_reactions": QUICK_REACTIONS,
        "qna_sessions": qna_sessions,
        "current_qna_filter": int(qna_filter_id) if qna_filter_id and qna_filter_id.isdigit() else None,
    }
    return render(request, "main/dashboard.html", context)


@login_required
def reply_message(request, message_id):
    """Menyimpan balasan dari pengguna dan mempublikasikan pesan."""
    msg = get_object_or_404(Message, id=message_id, recipient=request.user)

    if request.method == "POST":
        form = ReplyForm(request.POST, instance=msg)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.replied_at = timezone.now()
            reply.is_public = True
            reply.is_read = True
            reply.save()
            messages.success(request, _("Balasan terkirim."))

    return redirect("dashboard")


@login_required
def delete_message(request, message_id):
    """Menghapus pesan dari database secara permanen."""
    if request.method == "POST":
        msg = get_object_or_404(Message, id=message_id, recipient=request.user)
        msg.delete()
        messages.success(request, _("Pesan dihapus."))
    return redirect("dashboard")


@login_required
def reveal_disposable_message(request, message_id):
    """Menampilkan pesan mode 'Sekali Baca' lalu menghancurkannya (Self-Destruct)."""
    # Wajibkan POST agar bot/crawler tidak menghapus pesan secara otomatis
    if request.method != "POST":
        messages.warning(
            request, _("Gunakan tombol resmi untuk membuka pesan sekali baca.")
        )
        return redirect("dashboard")

    msg = get_object_or_404(
        Message, id=message_id, recipient=request.user, is_disposable=True
    )

    # Salin data sebelum dihapus
    context = {
        "content": msg.content,
        "sender_device": msg.sender_device,
        "sender_browser": msg.sender_browser,
        "created_at": msg.created_at.strftime("%d %b %Y, %H:%M"),
    }

    # Self-Destruct sekarang aman dari intipan Bot
    msg.delete()
    return render(request, "main/reveal_message.html", context)


@login_required
def block_sender(request, message_id):
    """Memblokir IP pengirim pesan agar tidak bisa mengirim pesan lagi."""
    msg = get_object_or_404(Message, id=message_id, recipient=request.user)

    if msg.sender_ip:
        BlockList.objects.get_or_create(user=request.user, ip_address=msg.sender_ip)
        messages.warning(request, _("Pengirim telah diblokir."))
    else:
        messages.error(request, _("Gagal memblokir: IP tidak ditemukan."))

    return redirect("dashboard")


@login_required
def toggle_favorite(request, message_id):
    """Menyematkan (Pin) atau melepas sematan pada pesan."""
    msg = get_object_or_404(Message, id=message_id, recipient=request.user)
    msg.is_favorite = not msg.is_favorite
    msg.save()

    status = "dipin" if msg.is_favorite else "dilepas"
    status_translated = _("dipin") if msg.is_favorite else _("dilepas")
    messages.success(
        request, _("Pesan berhasil %(status)s.") % {"status": status_translated}
    )
    return redirect("dashboard")


@login_required
def set_reaction(request, message_id, emoji):
    """Menambahkan reaksi emoji cepat pada pesan dan mempublikasikannya."""
    msg = get_object_or_404(Message, id=message_id, recipient=request.user)

    if emoji == "remove":
        msg.reaction = ""
        msg.save()
        messages.success(request, _("Reaksi dihapus."))
    else:
        msg.reaction = emoji
        msg.is_public = True
        msg.is_read = True
        msg.save()
        messages.success(
            request, _("Kamu bereaksi %(emoji)s pada pesan rahasia.") % {"emoji": emoji}
        )

    return redirect("dashboard")


@login_required
def edit_profile(request):
    """Menangani pembaruan data profil pengguna (Bio, Avatar, Tema)."""
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            # --- UPDATE LANGUAGE SESSION ---
            from django.utils import translation

            user_language = profile.preferred_language
            translation.activate(user_language)
            request.session["_language"] = user_language

            messages.success(request, _("Profil diperbarui."))
            return redirect("dashboard")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "main/edit_profile.html", {"form": form})


@login_required
def analytics_dashboard(request):
    """Mengolah dan menampilkan data analitik pesan masuk pengguna."""
    user_id = request.user.id
    base_query = Message.objects.filter(recipient_id=user_id)

    # 1. Key Performance Indicators (KPIs)
    total_messages = base_query.count()
    unread_messages = base_query.filter(is_read=False).count()

    replied_messages = (
        base_query.exclude(reply_content__exact="")
        .exclude(reply_content__isnull=True)
        .count()
    )
    reply_rate = (
        round((replied_messages / total_messages) * 100, 1) if total_messages > 0 else 0
    )

    public_messages = base_query.filter(is_public=True).count()
    share_rate = (
        round((public_messages / total_messages) * 100, 1) if total_messages > 0 else 0
    )

    # 2. Tren Waktu (7 Hari Terakhir)
    sevendays_ago = timezone.now() - timezone.timedelta(days=7)
    daily_counts = (
        base_query.filter(created_at__gte=sevendays_ago)
        .annotate(date=TruncDate("created_at"))
        .values("date")
        .annotate(count=Count("id"))
        .order_by("date")
    )

    trend_data = json.dumps(
        {
            "labels": [item["date"].strftime("%d %b") for item in daily_counts],
            "data": [item["count"] for item in daily_counts],
        }
    )

    # 3. Waktu Emas (Peak Active Hours)
    hour_distribution = (
        base_query.annotate(hour=ExtractHour("created_at"))
        .values("hour")
        .annotate(count=Count("id"))
        .order_by("hour")
    )

    hours_counts = [0] * 24
    for item in hour_distribution:
        if item["hour"] is not None:
            hours_counts[item["hour"]] = item["count"]

    peak_hours_data = json.dumps(
        {"labels": [f"{str(i).zfill(2)}:00" for i in range(24)], "data": hours_counts}
    )

    # 4. Sentimen Reaksi (Emoji Analytics)
    reaction_dist = (
        base_query.exclude(reaction__exact="")
        .exclude(reaction__isnull=True)
        .values("reaction")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    reaction_data = json.dumps(
        {
            "labels": [item["reaction"] for item in reaction_dist],
            "data": [item["count"] for item in reaction_dist],
        }
    )

    # 5. Distribusi OS & Browser
    os_dist = (
        base_query.exclude(sender_device__exact="")
        .exclude(sender_device__isnull=True)
        .values("sender_device")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    os_data = json.dumps(
        {
            "labels": [item["sender_device"] for item in os_dist],
            "data": [item["count"] for item in os_dist],
        }
    )

    browser_dist = (
        base_query.exclude(sender_browser__exact="")
        .exclude(sender_browser__isnull=True)
        .values("sender_browser")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    browser_data = json.dumps(
        {
            "labels": [item["sender_browser"] for item in browser_dist],
            "data": [item["count"] for item in browser_dist],
        }
    )

    context = {
        "total_messages": total_messages,
        "unread_messages": unread_messages,
        "reply_rate": reply_rate,
        "share_rate": share_rate,
        "trend_data": trend_data,
        "peak_hours_data": peak_hours_data,
        "reaction_data": reaction_data,
        "os_data": os_data,
        "browser_data": browser_data,
    }

    return render(request, "main/analytics.html", context)


@login_required
def api_check_new_messages(request):
    """API Endpoint untuk mengecek pesan baru via AJAX Polling."""
    last_id = request.GET.get("last_id", 0)
    try:
        last_id = int(last_id)
    except ValueError:
        last_id = 0

    new_messages = Message.objects.filter(
        recipient=request.user, id__gt=last_id
    ).order_by("created_at")

    if not new_messages.exists():
        return JsonResponse({"status": "no_new_messages"})

    # Render HTML untuk setiap pesan baru
    # Urutan ascending (created_at), jadi pesan paling baru dirender terakhir,
    # dan ditambahkan ke depan string (prepend) agar di HTML muncul paling atas.
    html_content = ""
    for msg in new_messages:
        rendered_html = render_to_string(
            "main/partials/message_card.html",
            {"msg": msg, "quick_reactions": QUICK_REACTIONS, "user": request.user},
            request=request,
        )
        html_content = rendered_html + html_content

    latest_id = new_messages.last().id

    return JsonResponse(
        {
            "status": "success",
            "html": html_content,
            "latest_id": latest_id,
            "count": new_messages.count(),
        }
    )


# ==============================================================================
# ERROR HANDLERS
# ==============================================================================


def ratelimit_error_handler(request, exception=None):
    """
    Menangkap error 403. Jika dari Rate Limit, kembalikan flash message.
    Jika error 403 generik (Akses Ditolak), tampilkan halaman 403 Premium.
    """
    if exception and exception.__class__.__name__ == 'Ratelimited':
        referer = request.META.get("HTTP_REFERER", "/")
        messages.error(
            request,
            _(
                "Tunggu sebentar! Kamu mengakses fitur ini terlalu cepat. Silakan coba lagi dalam 1 menit."
            ),
        )
        return redirect(referer)
    
    # Jika bukan dari ratelimit, tampilkan halaman 403 standar
    return render(request, "403.html", status=403)


def csrf_failure(request, reason=""):
    """Menangkap error 403 CSRF dan menampilkan desain halaman error khusus."""
    return render(request, "main/403_csrf.html", status=403)


def privacy_page(request):
    """Menampilkan halaman statis Kebijakan Privasi (Syarat AdSense)."""
    return render(request, "main/privacy.html")


@login_required
def create_qna_session(request):
    """Membuat Sesi QnA baru."""
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            QnASession.objects.create(user=request.user, title=title)
            messages.success(request, _("Tautan QnA Spesifik berhasil dibuat! 🚀"))
        else:
            messages.error(request, _("Topik pertanyaan tidak boleh kosong."))
    return redirect("dashboard")


@login_required
def toggle_qna_status(request, qna_id):
    """Mengubah status aktif Sesi QnA."""
    qna = get_object_or_404(QnASession, id=qna_id, user=request.user)
    if request.method == "POST":
        qna.is_active = not qna.is_active
        qna.save()
        status = _("Diaktifkan") if qna.is_active else _("Ditutup")
        messages.success(request, _("Tautan QnA berhasil %s.") % status)
    return redirect("dashboard")


@login_required
def delete_qna_session(request, qna_id):
    """Menghapus Sesi QnA."""
    qna = get_object_or_404(QnASession, id=qna_id, user=request.user)
    if request.method == "POST":
        qna.delete()
        messages.success(request, _("Tautan QnA dihapus secara permanen."))
    return redirect("dashboard")
