from django import forms

from .models import UserReply


class ReplyForm(forms.ModelForm):
    class Meta:
        model = UserReply
        fields = [
            'content',
        ]
