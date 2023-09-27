from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Comment)
admin.site.register(Media)
admin.site.register(CustomUser)
admin.site.register(SingleMedia)
admin.site.register(MultiMedia)
admin.site.register(VideoPlayList)
# admin.site.register(Followers)
# admin.site.register(Following)
admin.site.register(RequestList)
admin.site.register(Request)