from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Message, Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text=_(
            "Wajib diisi. Email ini diperlukan jika suatu saat kamu lupa password."
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                _("Email ini sudah terdaftar. Silakan gunakan email lain.")
            )
        return email


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Email / Username"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg rounded-pill glass-input",
                "placeholder": _("Email atau Username"),
            }
        ),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg rounded-pill glass-input",
                "placeholder": "••••••••",
            }
        ),
    )


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["reply_content"]
        widgets = {
            "reply_content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Tulis balasanmu di sini..."),
                    "rows": 3,
                }
            ),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "avatar", "theme_color", "preferred_language"]
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Tulis kata sambutan untuk profilmu..."),
                    "rows": 3,
                }
            ),
            "theme_color": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color w-100",
                    "title": _("Pilih warna tema"),
                }
            ),
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
            "preferred_language": forms.Select(attrs={"class": "form-select"}),
        }
