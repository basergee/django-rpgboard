from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import UserReply, Post


class ReplyForm(forms.ModelForm):
    class Meta:
        model = UserReply
        fields = [
            'content',
        ]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'post_type',
            'content',
            'upload',
        ]


class UserSignupForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("username",
                  "email",
                  "password1",
                  "password2",
                  )
