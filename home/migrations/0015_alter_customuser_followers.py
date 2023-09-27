# Generated by Django 4.2 on 2023-09-27 06:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_remove_following_following_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='followers',
            field=models.ManyToManyField(null=True, related_name='user_followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
