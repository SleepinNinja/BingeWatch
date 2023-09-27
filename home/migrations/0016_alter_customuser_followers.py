# Generated by Django 4.2 on 2023-09-27 06:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_customuser_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='followers',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_followers', to=settings.AUTH_USER_MODEL),
        ),
    ]