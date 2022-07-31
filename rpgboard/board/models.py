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

    author = models.OneToOneField(User, on_delete=models.CASCADE)
    post_type = models.CharField(
        max_length=2,
        choices=post_types,
        default='TK'
    )
    title = models.TextField()
    content = models.TextField()
    upload = models.FileField(upload_to='uploads/')
    creation_time = models.DateTimeField(auto_now_add=True)
