from django.contrib import admin

# Register your models here.
from .models import ShoppingCart, OrderInfo ,OrderGoods

admin.site.register(ShoppingCart)

admin.site.register(OrderInfo)

admin.site.register(OrderGoods)
