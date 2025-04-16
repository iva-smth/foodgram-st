# views.py
from rest_framework import viewsets 
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
)

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from users.models import Subscribtion
from recipes.models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .pagination import CustomPagination
from rest_framework.pagination import LimitOffsetPagination
User = get_user_model()

class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer = UserSerializer()
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    
class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, 
                       filters.SearchFilter,
                    )
    filterset_fields = ('name',)
    search_fields = ('^name',) 


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = []
    
    def get_serializer_class(self):
        """Метод для вызова определенного сериализатора. """

        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        elif self.action in ('create', 'partial_update'):
            return 

    def get_serializer_context(self):
        """Метод для передачи контекста. """

        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
