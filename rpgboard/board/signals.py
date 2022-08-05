import logging
from datetime import datetime, timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

from rpgboard.settings import DEFAULT_FROM_EMAIL
from .models import UserReply, Post, UserConfirmCodes


logger = logging.getLogger(__name__)


@receiver(post_save, sender=UserReply)
def notify_author_when_reply_is_created(instance, created, **kwargs):
    if created:
        author = instance.post.author.username
        email_to = instance.post.author.email
        title = instance.post.title
        message = f'Здравствуйте, {author}. На ваше объявление с заголовком ' \
                  f'\"{title}\" получен отклик. Посмотреть и принять или ' \
                  f'удалить отклик Вы можете в Личном кабинете'

        logger.info(message)

        # send_mail(
        #     subject='Новый отклик',
        #     message=message,
        #     from_email=DEFAULT_FROM_EMAIL,
        #     recipient_list=[f'{email_to}']
        # )


@receiver(post_save, sender=UserReply)
def notify_when_reply_accepted(instance, **kwargs):
    if instance.is_accepted:
        # Отправим сообщение пользователю, оставившему отклик
        reply_author = instance.reply_author.username
        reply_author_email = instance.reply_author.email

        logger.info(reply_author)
        logger.info(reply_author_email)
        logger.info(f'Здравствуйте, {reply_author}. Ваш отклик на объявление '
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
        logger.info(message)

        # send_mail(
        #     subject='Новое объявление',
        #     message=message,
        #     from_email=DEFAULT_FROM_EMAIL,
        #     recipient_list=[f'{reply_author_email}']
        # )


def generate_confirm_code():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return get_random_string(4, chars)


@receiver(post_save, sender=User)
def create_user_confirmcodes(sender, instance, created, **kwargs):
    logger.info('user create')
    if created:
        # Генерируем код и проверяем его уникальность
        code = generate_confirm_code()
        while UserConfirmCodes.objects.filter(code=code).exists():
            code = generate_confirm_code()
        expdate = datetime.strftime(
            datetime.now() + timedelta(minutes=5), "%Y-%m-%d %H:%M:%S"
        )
        usc = UserConfirmCodes.objects.create(
            user=instance,
            code=code,
            code_expires=expdate
        )
        usc.save()

        # Отправляем код на почту пользователя
        message = f'Ваш код подтверждения: {code}'
        to_email = instance.email

        logger.info(message)
        logger.info(f'Отправляем на {to_email}')

        # send_mail(
        #     subject='Код подтверждения',
        #     message=message,
        #     from_email=DEFAULT_FROM_EMAIL,
        #     recipient_list=[f'{to_email}']
        # )


@receiver(post_save, sender=User)
def save_user_confirmcodes(sender, instance, **kwargs):
    logger.info('user save')
    if not instance.is_active:
        # Добавил это условие из-за того, что при авторизации единственным
        # самым первым пользователем (admin) вылетело исключение, сообщающее,
        # что userconfirmcodes не существует. Самый первый пользователь был
        # создан не через форму регистрации, поэтому с ним нет связанного кода
        instance.userconfirmcodes.save()
