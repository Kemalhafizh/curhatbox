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
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tulis kata sambutan untuk profilmu...',
                'rows': 3
            }),
        }