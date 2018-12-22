from django.db import models
from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Goods

User = get_user_model()


# Create your models here.

class ShoppingCart(models.Model):
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name='goods', on_delete=models.CASCADE)
    nums = models.IntegerField(default=0, verbose_name="the quantity")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add time")

    class Meta:
        verbose_name = "shoppingcart"
        verbose_name_plural = verbose_name
        unique_together = ('user', 'goods')

    def __str__(self):
        return "%s(%d)".format(self.goods.name, self.nums)


class OrderInfo(models.Model):
    ORDER_STATUS = (('SUCCESS', 'SUCCESS'),
                    ('CLOSED', 'CLOSED'),
                    ('WAIT_PAY', 'WAIT_PAY'),
                    ('FINISHED', 'FINISHED'),
                    ('PAYING', 'PAYING'),
                    )

    user = models.ForeignKey(User, verbose_name="user",on_delete=models.CASCADE)
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="order id")
    trade_no = models.CharField(max_length=100, null=True, blank=True, verbose_name="trade id")
    pay_status = models.CharField(choices=ORDER_STATUS, default='PAYING', max_length=30, verbose_name="status")
    post_script = models.CharField(max_length=200, verbose_name="message")
    order_mount = models.FloatField(default=0, verbose_name="the quantity")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="pay time")

    address = models.CharField(max_length=100, default="", verbose_name="address")
    signer_name = models.CharField(max_length=20, default="", verbose_name="who sign the bill")
    signer_mobile = models.CharField(max_length=20, verbose_name='the phone number')

    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "order "
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    order = models.ForeignKey(OrderInfo, related_name="goods", on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    goods_num = models.IntegerField(default=0)

    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "goods in order"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
