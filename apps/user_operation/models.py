from django.db import models

from django.db import models
from django.contrib.auth import get_user_model, get_permission_codename
from datetime import  datetime

from goods.models import Goods

User = get_user_model()


# Create your models here.

class UserFav(models.Model):
    """
    user favorite
    """
    user = models.ForeignKey(User, verbose_name="user",on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name="goods", help_text="goods id", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add time")

    class Meta:
        verbose_name = "user favorite"
        verbose_name_plural  = verbose_name
        unique_together =("user", "goods")

    def __str__(self):
        return self.user.name
