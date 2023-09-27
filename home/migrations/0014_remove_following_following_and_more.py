# Generated by Django 4.2 on 2023-09-27 06:25

from django.conf import settings
from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20230409_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='following',
            name='following',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='followers_count',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='following_count',
        ),
        migrations.RemoveField(
            model_name='multimedia',
            name='episode_count',
        ),
        migrations.AddField(
            model_name='customuser',
            name='followers',
            field=models.ManyToManyField(related_name='user_followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='singlemedia',
            name='genre',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('AC', 'Action'), ('AD', 'Adventure'), ('CO', 'Comedy'), ('CRMY', 'Crime and Mystery'), ('FA', 'Fantasy'), ('HI', 'Historical'), ('HO', 'Horror'), ('RO', 'Romance'), ('SCFI', 'Science Fiction'), ('TH', 'Thriller'), ('OT', 'Other')], max_length=10, verbose_name='Genre'),
        ),
        migrations.AlterField(
            model_name='singlemedia',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='videoplaylist',
            name='genre',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('AC', 'Action'), ('AD', 'Adventure'), ('CO', 'Comedy'), ('CRMY', 'Crime and Mystery'), ('FA', 'Fantasy'), ('HI', 'Historical'), ('HO', 'Horror'), ('RO', 'Romance'), ('SCFI', 'Science Fiction'), ('TH', 'Thriller'), ('OT', 'Other')], max_length=10, verbose_name='Genre'),
        ),
        migrations.DeleteModel(
            name='Followers',
        ),
        migrations.DeleteModel(
            name='Following',
        ),
    ]