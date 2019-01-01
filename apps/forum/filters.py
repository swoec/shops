import django_filters
from django.db.models import Q

from .models import Topic, Video, Image, Comments, Category


class TopicFilter(django_filters.rest_framework.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    content = django_filters.CharFilter(field_name='context', lookup_expr='icontains')
    add_time = django_filters.DateTimeFilter(field_name='add_time', lookup_expr='gte')

    class Meta:
        models = Topic
        fields = ('title', 'content', 'add_time')
