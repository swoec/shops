import time
from abc import ABCMeta

from rest_framework import serializers
from .models import OrderInfo, ShoppingCart, OrderGoods, Goods
from goods.serializers import GoodsSerializers




class ShopCartDetailSerializer(serializers.Serializer):
    goods = GoodsSerializers(many=False, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ('goods', 'nums')


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    nums = serializers.IntegerField(required=True, label="quantity", min_value=1,
                                    error_messages={
                                        "min_value": "large than one",
                                        "required": "please add more quantity"
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validate_date):
        user = self.context['request'].user
        nums = validate_date['nums']
        goods = validate_date['goods']

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validate_date)

        return existed

    def update(self, instance, validate_data):
        instance.nums = validate_data['nums']
        instance.save()
        return instance


class OrderGoodsSerializer(serializers.Serializer):
    goods = GoodsSerializers(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def generate_order_sn(self):
        # 当前时间+userid+随机数
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))

        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
