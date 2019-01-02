from .models import Topic, Comments, Category, Video, Image
from rest_framework import serializers
from django.contrib.auth import get_user_model
import re
from Moocshop.settings import REGEX_IMAGE, REGEX_VIDEO

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )
    image = ImageSerializer(many=True, read_only=True)
    video = VideoSerializer(many=True, read_only=True)

    #category = CategorySerializer(many=False, read_only=True)

    comments = CommentsSerializer(many=True, read_only=True)

    def validate_title(self, title):
        print(title)
        return title

    class Meta:
        model = Topic
        # fields = ('image','video', 'comments' )
        # fields = '__all__'
        fields = ('image', 'video', 'comments', 'title', 'context', 'user', 'category', 'add_time')

    def create(self, validated_data):

        user = validated_data['user']
        topic = Topic.objects.create(title=validated_data['title'], context=validated_data['context'],
                                     category=validated_data['category'], user=validated_data['user'])

        files = self.context.get('view').request.FILES

        for image in files.getlist('image'):

            if not re.match(REGEX_IMAGE, image.name):
                raise serializers.ValidationError("false image format")
            Image.objects.create(topic=topic, image=image, user=user)

        for video in files.getlist('video'):
            if not re.match(REGEX_VIDEO, video.name):
                raise serializers.ValidationError("false video format")

            Video.objects.create(topic=topic, video=video, user=user)

        return topic


class TopicsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'
