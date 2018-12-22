
from rest_framework import serializers
from .models import UserFav
from goods.serializers import GoodsSerializers
from rest_framework.validators import UniqueTogetherValidator


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializers()

    class Meta:
        model = UserFav
        fields = ("goods","id")


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserFav
        validators = [UniqueTogetherValidator(queryset=UserFav.objects.all(),
                                              fields=('user','goods'),
                                              message="add to favorite")
                      ]
        fields = ("user","goods","id")
