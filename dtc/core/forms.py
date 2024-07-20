from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "password1",
            "password2",
        )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("content",)
        labels = {
            "content": "No que você está pensando?",
        }
