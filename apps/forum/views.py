from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import authentication, status
from rest_framework import permissions
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from django_filters.rest_framework import DjangoFilterBackend
from .models import Topic, Category, Video, Image, Comments
from .serializers import TopicSerializer, TopicsCreateSerializer, CommentsSerializer
from .filters import TopicFilter
from utils.permissions import IsOwnerOrReadOnly


class TopicPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'p'
    page_size_query_param = 'page_size'
    max_page_size = 100


# Create your views here.

class TopicListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    pagination_class = TopicPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    filter_class = TopicFilter
    search_fields = ('title', 'context', 'add_time')
    ordering_fields = ('title', 'add_time')

    parser_classes = (MultiPartParser,)

    #
    # def get_queryset(self):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # return queryset
        # for q in queryset:
        #     q.model.image_set = Image.objects.filter(topic=q.id)
        #     q.model.video_set = Video.objects.filter(topic=q.id)
        #     q.model.comments_st = Comments.objects.filter(topic=q.id)
        # q.save()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for q in serializer.data:
                q.image = Image.objects.filter(topic=q['id'])
                q.video = Video.objects.filter(topic=q['id'])
                q.comments = Comments.objects.filter(topic=q['id'])

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        for q in serializer.data:
            q.image = Image.objects.filter(topic=q['id'])
            q.video = Video.objects.filter(topic=q['id'])
            q.comments = Comments.objects.filter(topic=q['id'])
            # serializer.data.append(q)

        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def add_value(self, request, id = None):
        # queryset = Topic.objects.
        queryset = Topic.objects.filter(id=id)
        serializer = self.get_serializer(queryset, many=True)
        for q in serializer.data:
            q.image = Image.objects.filter(topic=q['id'])
            q.video = Video.objects.filter(topic=q['id'])
            q.comments = Comments.objects.filter(topic=q['id'])


        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.image = Image.objects.filter(topic=instance.id)
        instance.video = Video.objects.filter(topic=instance.id)
        instance.comments = Comments.objects.filter(topic=instance.id)

        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    # def post(self, request, format=None):
    #     """
    #
    #     :param request:
    #     :param format:
    #     """
    #     files = request.FILES.getlist('video', None)
    #
    #     image = Image()


class TopicCreateViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicsCreateSerializer
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TopicSerializer
        elif self.action == 'create':
            return TopicsCreateSerializer

        return TopicSerializer

    def get_queryset(self):
        return Topic.objects.all()

    def get_permissions(self):

        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action == 'retrieve':
            return []

        return []

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        topic = self.perform_create(serializer)

        re_dict = serializer.data
        header = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED)


class CommentsViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = {'topic'}
