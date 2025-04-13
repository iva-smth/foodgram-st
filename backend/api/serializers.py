from django.contrib.auth import get_user_model
from recipes.models import Ingredient, Recipe, RecipeIngredient, Favourite, ShoppingList
from users.models import Subscribtion
from rest_framework import serializers
from rest_framework.fields import IntegerField, SerializerMethodField
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import status
from rest_framework.exceptions import ValidationError

User = get_user_model()

class UserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, creator):
        subscriber = self.context.get('request').user
        if subscriber.is_anonymous:
            return False
        return Subscribtion.objects.filter(creator=creator, subscriber=subscriber).exists()


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )

