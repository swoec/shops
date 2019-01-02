from django.db import models

from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()


# Create your models here.

class Category(models.Model):
    CATEGORY_TYPE = (
        (1, 'math'),
        (2, 'science'),
        (3, 'nature'),
        (4, 'music'),
    )
    name = models.CharField(max_length=40, verbose_name="catogary name")
    add_time = models.DateTimeField(auto_now=True)
    desc = models.TextField(max_length=200, null=True, blank=True)
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="category id")

    class Meta:
        verbose_name = "category"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Topic(models.Model):
    title = models.CharField(max_length=80, null=False, blank=False, verbose_name="topic title")
    context = models.TextField(max_length=500, verbose_name='topic content')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now=True)
    # image = models.ManyToManyField(Image, related_name='image')
    # video = models.ManyToManyField(Video, related_name='video')
    # comments = models.ManyToManyField(Comments, related_name='comments')


    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title



class Image(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='topic/', verbose_name='image ', null=True, blank=True)
    add_time = models.DateTimeField(auto_now=True, verbose_name="add time")

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.topic.title


class Video(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.FileField(upload_to='topic/video/', verbose_name='video', null=True, blank=True)
    add_time = models.DateTimeField(auto_now=True, verbose_name='upload time')


    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.topic.title


class Comments(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=200, null=True, blank=True, verbose_name='comments content')
    add_time = models.DateTimeField(auto_now=True)
    relative_comment = models.ForeignKey('self', null=True, blank=True, verbose_name='reply',
                                         on_delete=models.CASCADE, related_name='sub_comment')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = verbose_name

    def __str__(self):
        self.title = self.topic.title
        return self.content


