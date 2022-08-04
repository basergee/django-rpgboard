from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from tinymce.widgets import TinyMCE

from .models import UserReply, Post


class ReplyForm(forms.ModelForm):
    class Meta:
        model = UserReply
        fields = [
            'content',
        ]


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

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


class UserConfirmCodeForm(forms.Form):
    code = forms.CharField(max_length=4)
