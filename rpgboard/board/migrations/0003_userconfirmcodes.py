# Generated by Django 4.0.6 on 2022-08-03 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0002_alter_post_upload'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserConfirmCodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_confirmed', models.BooleanField(default=False)),
                ('code', models.CharField(max_length=4)),
                ('code_expires', models.DateTimeField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
