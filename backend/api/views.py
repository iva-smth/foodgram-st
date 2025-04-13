# views.py
from rest_framework import viewsets 
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from users.models import Subscribtion

User = get_user_model()

class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    