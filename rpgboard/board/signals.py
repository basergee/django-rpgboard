from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User

from rpgboard.settings import DEFAULT_FROM_EMAIL
from .models import UserReply, Post


@receiver(post_save, sender=UserReply)
def notify_when_reply_accepted(instance, **kwargs):
    if instance.is_accepted:
        # Отправим сообщение пользователю, оставившему отклик
        reply_author = instance.reply_author.username
        reply_author_email = instance.reply_author.email

        print(reply_author)
        print(reply_author_email)
        print(f'Здравствуйте, {reply_author}. Ваш отклик на объявление '
              f'\"{instance.post.title}\" принят')

        # send_mail(
        #     subject='Отклик принят',
        #     message=f'Здравствуйте, {reply_author}. Ваш отклик на объявление '
        #             f'\"{instance.post.title}\" принят',
        #     from_email=DEFAULT_FROM_EMAIL,
        #     recipient_list=[f'{reply_author_email}']
        # )


@receiver(post_save, sender=Post)
def notify_about_new_post(instance, **kwargs):
    for u in User.objects.all():
        if u == instance.author:
            # Не отправляем сообщение автору объявления
            continue
        message = f'Здравствуйте, {u.username}. Появилось новое объявление: ' \
                  f'{instance.title}\n\n{instance.content}'
        print(message)

        # send_mail(
        #     subject='Новое объявление',
        #     message=message,
        #     from_email=DEFAULT_FROM_EMAIL,
        #     recipient_list=[f'{reply_author_email}']
        # )
