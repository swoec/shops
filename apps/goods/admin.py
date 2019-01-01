from django.contrib import admin

# Register your models here.

from .models import  Goods, GoodsImage, GoodsCategory, GoodsCategoryBrand

admin.site.register(GoodsCategory)

admin.site.register(Goods)

admin.site.register(GoodsImage)

admin.site.register(GoodsCategoryBrand)
