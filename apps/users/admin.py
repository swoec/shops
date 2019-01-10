from django.contrib import admin

# Register your models here.

from .models import UserProfile, VerifyCode, Citizen, Position

admin.site.register(UserProfile)

admin.site.register(VerifyCode)
admin.site.register(Citizen)
admin.site.register(Position)
