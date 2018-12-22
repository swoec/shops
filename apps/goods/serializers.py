from rest_framework import serializers
from django.db.models import Q
from .models import Goods, GoodsCategoryBrand, GoodsCategory, GoodsImage


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodsSerializers(serializers.ModelSerializer):
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)


    class Meta:
        model = Goods
        fields = "__all__"


class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "_all__"
