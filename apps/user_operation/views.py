from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from apps.utils.permissions import IsOwnerOrReadOnly

from .models import UserFav
from .serializers import UserFavDetailSerializer, UserFavSerializer


# Create your views here.

class UserFavPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class UserFavListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer

        return UserFavSerializer
