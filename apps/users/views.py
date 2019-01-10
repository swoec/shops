from django.shortcuts import render

from django.contrib.auth.backends import ModelBackend
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from .models import UserProfile, Citizen, Position
from .serializers import UserSerializer, CitizenSerializer, PositionSerializer, UserAddSerializer


# User = get_user_model()


# Create your views here.

class UserViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


class CitizenViewset(viewsets.ModelViewSet):
    queryset = Citizen.objects.all()
    serializer_class = CitizenSerializer


class PositionViewset(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class UseraddViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAddSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):

        return serializer.save()
