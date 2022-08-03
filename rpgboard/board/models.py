from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    post_types = (
        ('TK', 'Танки'),
        ('HL', 'Хилы'),
        ('DD', 'ДД'),
        ('TR', 'Торговцы'),
        ('GM', 'Гилдмастеры'),
        ('QG', 'Квестгиверы'),
        ('SM', 'Кузнецы'),
        ('TN', 'Кожевники'),
        ('PT', 'Зельевары'),
        ('SM', 'Мастера заклинаний'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type = models.CharField(
        max_length=2,
        choices=post_types,
        default='TK'
    )
    title = models.TextField()
    content = models.TextField()
    upload = models.FileField(upload_to='uploads/', blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)


class UserReply(models.Model):
    # Пользователь, который оставил отклик
    reply_author = models.ForeignKey(User, on_delete=models.CASCADE)

    # Объявление, на которое оставлен отклик
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # Текст отклика
    content = models.TextField()

    # Принят ли отклик пользователем, который создал объявление
    is_accepted = models.BooleanField(default=False)

    creation_time = models.DateTimeField(auto_now_add=True)


class UserConfirmCodes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    code = models.CharField(max_length=4)
    code_expires = models.DateTimeField()
