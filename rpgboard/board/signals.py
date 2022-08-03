from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserReply


@receiver(post_save, sender=UserReply)
def notify_when_reply_accepted(instance, **kwargs):
    print('Maybe accepted post...', instance)
