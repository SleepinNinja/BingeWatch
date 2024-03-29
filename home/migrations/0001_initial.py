# Generated by Django 3.2.6 on 2023-01-21 08:54

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='User ID')),
                ('followers_count', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('private', models.BooleanField(default=False)),
                ('following_count', models.PositiveIntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='WishList Id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VideoPlayList',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('genre', multiselectfield.db.fields.MultiSelectField(choices=[('AC', 'Action'), ('AD', 'Adventure'), ('CO', 'Comedy'), ('CRMY', 'Crime and Mystery'), ('FA', 'Fantasy'), ('HI', 'Historical'), ('HO', 'Horror'), ('RO', 'Romance'), ('SCFI', 'Science Fiction'), ('TH', 'Thriller'), ('OT', 'Other')], max_length=36, verbose_name='Genre')),
                ('quality', models.CharField(choices=[('2160p', '4K'), ('1440p', '2K'), ('1080p', 'Full HD'), ('720p', 'HD'), ('480p', 'SD')], max_length=5, verbose_name='Media Quality')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Media Description')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('media_type', models.CharField(choices=[('A', 'Anime'), ('W', 'WebSeries')], max_length=50, verbose_name='Type of Media')),
                ('uploader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_wishlist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.wishlist')),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
        migrations.CreateModel(
            name='UserPlayList',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='User Playlist Id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SingleMedia',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('genre', multiselectfield.db.fields.MultiSelectField(choices=[('AC', 'Action'), ('AD', 'Adventure'), ('CO', 'Comedy'), ('CRMY', 'Crime and Mystery'), ('FA', 'Fantasy'), ('HI', 'Historical'), ('HO', 'Horror'), ('RO', 'Romance'), ('SCFI', 'Science Fiction'), ('TH', 'Thriller'), ('OT', 'Other')], max_length=36, verbose_name='Genre')),
                ('quality', models.CharField(choices=[('2160p', '4K'), ('1440p', '2K'), ('1080p', 'Full HD'), ('720p', 'HD'), ('480p', 'SD')], max_length=5, verbose_name='Media Quality')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Media Description')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('media_type', models.CharField(choices=[('M', 'Movie')], default='Movie', max_length=50, verbose_name='Type of Media')),
                ('uploader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_wishlist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.wishlist')),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
        migrations.CreateModel(
            name='MultiMedia',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Season ID')),
                ('name', models.CharField(max_length=50, verbose_name='Season name')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Season Description')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('episode_count', models.PositiveIntegerField(verbose_name='No. of episodes')),
                ('playlist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.videoplaylist')),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Media ID')),
                ('name', models.CharField(max_length=500, verbose_name='Media Name')),
                ('upload_date', models.DateField(auto_now_add=True)),
                ('views', models.PositiveIntegerField(default=0, verbose_name='Media views')),
                ('likes', models.PositiveIntegerField(default=0, verbose_name='Likes')),
                ('dislikes', models.PositiveIntegerField(default=0, verbose_name='Dislikes')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='Media Price')),
                ('multi_media', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.multimedia')),
                ('single_media', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.singlemedia')),
            ],
            options={
                'ordering': ['upload_date'],
            },
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('following', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Comment ID')),
                ('comment', models.TextField()),
                ('time', models.DateTimeField(auto_now=True)),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.media')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
