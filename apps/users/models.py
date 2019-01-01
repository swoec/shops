from django.db import models

# Create your models here.

from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class UserProfile(AbstractBaseUser):
    """
    UserProfile
    """
    name = models.CharField(max_length=80, null=True, blank=True, verbose_name="name")
    gender = models.CharField(max_length=6, choices=(("male","male"),("female","female")), default="female", verbose_name="gender")
    birthday = models.DateField(null=True, blank=True,verbose_name="birthday")
    address = models.CharField(max_length=120, null=True, blank=True, verbose_name="address")
    email = models.EmailField(max_length=120, null=True, blank=True, verbose_name="email")
    mobile = models.CharField(max_length=20,null=True, blank=True)

    class Meta:
        verbose_name = "user Profile"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class VerifyCode(models.Model):
    code = models.CharField(max_length=4)
    mobile = models.CharField(max_length=20)
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "verifycode"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code



