from django.contrib import admin

# Register your models here.

from .models import Category, Topic, Image, Video, Comments

# Register your models here.

admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Comments)
