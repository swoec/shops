from .models import Topic, Comments, Category, Video, Image
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=True, read_only=True)
    video = VideoSerializer(many=True, read_only=True)
    # comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        #fields = ('image','video', 'comments' )
        #fields = '__all__' #
        fields = ('image', 'video',  'title', 'context', 'user', 'category', 'add_time')

    def create(self, validated_data):
        title = validated_data['title']
        context = validated_data['context']
        category = validated_data['category']
        user = validated_data['user']
        # topic = Topic()
        # topic.title = title
        # topic.context = context
        # topic.category = category
        # topic.user = user
        topic = Topic.objects.create(title=validated_data['title'], context=validated_data['context'], category=validated_data['category'], user=validated_data['user'])

        files = self.context.get('view').request.FILES
        # topic = TopicSerializer.create(TopicSerializer(), validated_data=topic) #Topic.objects.create(topic)

        # for d in files.getlist('image'):
        #     te = d.name

        # for filename in files.get('image'):
        #     name = str(filename)

        for image in files.getlist('image'):
            Image.objects.create(topic=topic, image=image, user=user)

        # videos = self.context.get('view').request.FILES
        for video in files.getlist('video'):
            Video.objects.create(topic=topic, video=video, user=user)

        # comments = validated_data['comments']
        # for comment in comments:
        #     Comments.objects.update_or_create(topic=topic, content=comment)

        return topic


class TopicsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'
