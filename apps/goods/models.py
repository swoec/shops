from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField


# Create your models here.

class GoodsCategory(models.Model):
    """
    goods type
    """
    CATEGORY_TYPE = (
        (1, "CLASS 1"),
        (2, "CLASS 2"),
        (3, "CLASS 3"),
    )
    name = models.CharField(max_length=30, default="", verbose_name="name", help_text="catagory name")
    code = models.CharField(max_length=30, default="", verbose_name="code", help_text="catarogy code")
    desc = models.TextField(default="", verbose_name="", help_text="catagory description")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="category level",
                                        help_text="category level")
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="parent level",
                                        help_text="parent level",
                                        related_name="sub_cat", on_delete=models.CASCADE)
    is_tab = models.BooleanField(default=False, verbose_name="is navigator", help_text="is navigator")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add time")

    class Meta:
        verbose_name = "good catagory"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    brand
    """
    category = models.ForeignKey(GoodsCategory, related_name='brands', null=True, blank=True, verbose_name="category",
                                 on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=30, verbose_name="brand name", help_text="brand text")
    desc = models.TextField(default="", max_length=200, verbose_name="brand desc", help_text="brand desc")
    image = models.ImageField(max_length=200, upload_to="brands/")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add time")

    class Meta:
        verbose_name = "brands"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    category = models.ForeignKey(GoodsCategory, verbose_name="category", on_delete=models.CASCADE)
    goods_sn = models.CharField(max_length=50, default="", verbose_name="goods Id")
    name = models.CharField(max_length=100, verbose_name="goods name")
    click_num = models.IntegerField(default=0, verbose_name="click number")
    sold_num = models.IntegerField(default=0, verbose_name="sold number")
    fav_num = models.IntegerField(default=0, verbose_name="favorite number")
    goods_num = models.IntegerField(default=0, verbose_name="stock number")
    market_price = models.FloatField(default=0, verbose_name="market price")
    shop_price = models.FloatField(default=0, verbose_name="shop price")
    goods_brief = models.TextField(max_length=500, verbose_name="good description")
    goods_desc = UEditorField(verbose_name=u"内容", imagePath="goods/images/", width=1000, height=300,
                              filePath="goods/files/", default='')
    #goods_num = models.IntegerField(default=0)
    ship_free = models.BooleanField(default=True, verbose_name="need shipping fee or not")
    goods_front_image = models.ImageField(upload_to="goods/images/", null=True, blank=True,
                                          verbose_name="front page image")
    is_new = models.BooleanField(default=True, verbose_name="is new")
    is_hot = models.BooleanField(default=True, verbose_name="is hot")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add time")

    class Meta:
        verbose_name = "goods"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class GoodsImage(models.Model):

    goods = models.ForeignKey(Goods, verbose_name="商品", related_name="images",on_delete=models.CASCADE)
    image = models.ImageField(upload_to="", verbose_name="图片", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name
