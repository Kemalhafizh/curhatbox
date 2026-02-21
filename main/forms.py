from django import forms
from .models import Message, Profile

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['reply_content']
        widgets = {
            'reply_content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tulis balasanmu di sini...',
                'rows': 3
            }),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'theme_color']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tulis kata sambutan untuk profilmu...',
                'rows': 3
            }),
            'theme_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color w-100',
                'title': 'Pilih warna tema'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }