from django.db import models
from multiselectfield import MultiSelectField
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import uuid


class CustomUser(AbstractUser):
    uuid = models.UUIDField('User ID', default = uuid.uuid4, primary_key = True)
    followers_count = models.PositiveIntegerField(default = 0)
    profile_photo = models.ImageField(blank = True, null = True)
    description = models.TextField(max_length = 1000, blank = True, null = True)
    private = models.BooleanField(default = False)
    following_count = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return f'Username: {self.username}, name: {self.first_name + " " + self.last_name}'

    def get_absolute_url(self):
        return reverse('user_account', username = self.user.username)


class Followers(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null = True)


class Following(models.Model):
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null = True) 


class WishList(models.Model):
    uuid = models.UUIDField('WishList Id', default = uuid.uuid4, primary_key = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)


class BaseMedia(models.Model):
    MEDIA_QUALITY = (
        ('2160p', '4K'),
        ('1440p', '2K'),
        ('1080p', 'Full HD'),
        ('720p', 'HD'),
        ('480p', 'SD'),
    )

    MEDIA_TYPES = (
        ('M', 'Movie'),
        ('A', 'Anime'),
        ('W', 'WebSeries'),
    )

    MEDIA_GENRES = (
        ('AC', 'Action'),
        ('AD', 'Adventure'),
        ('CO', 'Comedy'),
        ('CRMY', 'Crime and Mystery'),
        ('FA', 'Fantasy'),
        ('HI', 'Historical'),
        ('HO', 'Horror'),
        ('RO', 'Romance'),
        ('SCFI', 'Science Fiction'),
        ('TH', 'Thriller'),
        ('OT', 'Other')
    )

    uuid = models.UUIDField('ID', default = uuid.uuid4, primary_key = True)
    name = models.CharField('Name', max_length = 100)
    genre = MultiSelectField('Genre', choices=MEDIA_GENRES, max_length=10)
    user_wishlist = models.ForeignKey(WishList, on_delete = models.CASCADE, null = True, blank = True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null = True)
    quality = models.CharField('Media Quality', max_length = 5, choices = MEDIA_QUALITY)
    description = models.TextField('Media Description', max_length = 1000, blank = True, null =True)
    date_created = models.DateTimeField('Created Date', auto_now_add = True)
    
    class Meta:
        abstract = True


class SingleMedia(BaseMedia): #movie
    media_type =  models.CharField('Type of Media', max_length = 50, default = 'Movie', choices = (BaseMedia.MEDIA_TYPES[0],))
    name = models.CharField('name', max_length = 100, blank = True, null = True)
    
    def save(self, *args, **kwargs):
        self.name = self.media.name 
        super().save(*args, **kwargs) 

    def get_absolute_url(self):
        return reverse('open_single_video', kwargs = {'search_value': self.name, 'video_uuid': self.media.uuid})

    class Meta:
        ordering = ['date_created']



def videoplaylist_file_storage(instance, filename):
    return f'{instance.uploader.username}\\{instance.get_media_type_display()}\\{instance.name}\\{filename}'

class VideoPlayList(BaseMedia):
    cover = models.ImageField(upload_to = videoplaylist_file_storage, blank = True, null = True)
    media_type = models.CharField('Type of Media', max_length = 50, choices = (BaseMedia.MEDIA_TYPES[1:3]))

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('open_playlist', kwargs = {'search_value': self.name, 'uuid': self.uuid})


def multimedia_file_storage(instance, filename):
    return f'{instance.playlist.uploader.username}\\{instance.playlist.get_media_type_display()}\\{instance.playlist.name}\\{filename}'

class MultiMedia(models.Model): # anime and web series
    cover = models.ImageField(upload_to = multimedia_file_storage, blank = True, null = True)
    uuid = models.UUIDField('Season ID', default = uuid.uuid4, primary_key = True)
    name = models.CharField('Season name', max_length = 50)
    description = models.TextField('Season Description', max_length = 1000, blank = True, null = True)
    playlist = models.ForeignKey(VideoPlayList, on_delete = models.CASCADE, null = True)
    date_created = models.DateTimeField(auto_now_add = True)
    #episode_count = models.PositiveIntegerField('No. of episodes')

    def get_absolute_url(self):
        return reverse('open_media', kwargs = {'search_value': self.playlist.name, 'season_name': self.name, 'season_uuid': self.uuid})
    
    def __str__(self):
        return self.name


#media_file_storage = FileSystemStorage(location = storage_location)
def media_file_storage(instance, filename):
    if instance.multi_media:
        return f'{instance.multi_media.playlist.uploader.username}\\{instance.multi_media.playlist.get_media_type_display()}\\{instance.multi_media.playlist.name}\\{instance.multi_media.name}\\{instance.name}\\{filename}' 

    return f'{instance.single_media.uploader.username}\\{instance.single_media.get_media_type_display()}\\{instance.name}\\{filename}' 

class Media(models.Model):
    uuid = models.UUIDField('Media ID', default = uuid.uuid4, primary_key = True)
    cover = models.ImageField('Media cover', upload_to = media_file_storage, blank = True, null = True)
    file = models.FileField('Media location', upload_to = media_file_storage, null = True, blank = True)
    name = models.CharField('Media Name', max_length = 500)
    upload_date = models.DateField(auto_now_add = True)
    views = models.PositiveIntegerField('Media views', default = 0)
    likes = models.PositiveIntegerField('Likes', default = 0)
    dislikes = models.PositiveIntegerField('Dislikes', default = 0)
    price = models.PositiveIntegerField('Media Price', default = 0)
    multi_media = models.ForeignKey(MultiMedia, on_delete = models.CASCADE, null = True, blank = True)
    single_media = models.OneToOneField(SingleMedia, on_delete = models.CASCADE, null = True, blank = True)


    def __str__(self):
        if self.multi_media:
            return self.multi_media.playlist.uploader.username + self.multi_media.playlist.get_media_type_display() + self.multi_media.playlist.name + self.multi_media.name + self.name

        return self.single_media.uploader.username + self.single_media.get_media_type_display() + self.name
        #return ''

    def get_absolute_url_multi_media(self):
        search_value = self.multi_media.playlist.name
        season_name = self.multi_media.name
        season_uuid = self.multi_media.uuid

        return reverse('open_video', kwargs = {'search_value': search_value, 'season_name': season_name, 'season_uuid': season_uuid, 'video_uuid': self.uuid})

    #def get_absolute_url_single_media(self):
    #    return reverse('')

    class Meta():
        ordering = ['upload_date',]

class Comment(models.Model):
    uuid = models.UUIDField('Comment ID', default = uuid.uuid4, primary_key = True)
    comment = models.TextField()
    time = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    media = models.ForeignKey(Media, on_delete = models.CASCADE)

    def __str__(self):
        return f'Comment: {self.comment}, User: {self.user.username}'


class UserPlayList(models.Model):
    uuid = models.UUIDField('User Playlist Id', default = uuid.uuid4, primary_key = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)


class RequestList(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null = True)


class Request(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    request_list = models.ForeignKey(RequestList, on_delete = models.CASCADE, null = True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    accepted = models.BooleanField(default = False)