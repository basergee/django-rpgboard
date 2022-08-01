from django import forms

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
