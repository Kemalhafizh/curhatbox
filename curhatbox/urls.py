"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView, TemplateView
from django.http import HttpResponse, FileResponse
import os

from django.contrib.auth import views as auth_views
from main.forms import CustomAuthenticationForm, AsyncPasswordResetForm
from main import views as main_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # --- AUTH / ACCOUNTS (Eksplisit dengan Template Premium) ---
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=CustomAuthenticationForm,
        ),
        name="login",
    ),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "accounts/password_reset/",
        main_views.CustomPasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.txt",
            html_email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            form_class=AsyncPasswordResetForm,
        ),
        name="password_reset",
    ),
    path(
        "accounts/password_reset/resend/",
        main_views.resend_password_reset_email,
        name="password_reset_resend",
    ),
    path(
        "accounts/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "accounts/", include("django.contrib.auth.urls")
    ),  # Fallback untuk sisa rute auth
    path("accounts/", include("allauth.urls")), # Rute Khusus untuk endpoint Google Oauth2
    path("login/", RedirectView.as_view(url="/accounts/login/", permanent=True)),
    path(
        "accounts/password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form.html"
        ),
        name="password_change",
    ),
    path(
        "accounts/password_change/request-reset/",
        main_views.trigger_reset_for_current_user,
        name="password_change_request_reset",
    ),
    path(
        "accounts/password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("i18n/", include("django.conf.urls.i18n")),  # Endpoint peranti bahasa
    path(
        "ads.txt",
        lambda r: FileResponse(
            open(os.path.join(settings.BASE_DIR, "ads.txt"), "rb"), content_type="text/plain"
        ),
    ),
    path(
        "robots.txt",
        lambda r: FileResponse(
            open(os.path.join(settings.BASE_DIR, "robots.txt"), "rb"), content_type="text/plain"
        ),
    ),
    path(
        "sitemap.xml",
        lambda r: FileResponse(
            open(os.path.join(settings.BASE_DIR, "sitemap.xml"), "rb"), content_type="text/xml"
        ),
    ),
    path(
        "googleejv9TLODICCbcW8QfmEyMrwfC6n8P0o71HMoTTbQqVk.html",
        lambda r: HttpResponse(
            "google-site-verification: googleejv9TLODICCbcW8QfmEyMrwfC6n8P0o71HMoTTbQqVk.html",
            content_type="text/html",
        ),
    ),
    # --- PWA URLs ---
    path(
        "manifest.json",
        TemplateView.as_view(
            template_name="main/manifest.json", content_type="application/json"
        ),
        name="manifest_json",
    ),
    path(
        "serviceworker.js",
        TemplateView.as_view(
            template_name="main/serviceworker.js", content_type="application/javascript"
        ),
        name="serviceworker_js",
    ),
    path(
        "offline/",
        TemplateView.as_view(template_name="main/offline.html"),
        name="offline",
    ),
    path(
        "google-site-verification=ejv9TLODICCbcW8QfmEyMrwfC6n8P0o71HMoTTbQqVk",
        lambda r: HttpResponse(
            "google-site-verification: ejv9TLODICCbcW8QfmEyMrwfC6n8P0o71HMoTTbQqVk",
            content_type="text/plain",
        ),
    ),
    path("", include("main.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = "main.views.ratelimit_error_handler"
