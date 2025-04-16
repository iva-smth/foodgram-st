from django.contrib.auth import get_user_model
from recipes.models import Ingredient, Recipe, RecipeIngredient, Favourite, ShoppingList
from users.models import Subscribtion
from rest_framework import serializers
from rest_framework.fields import IntegerField, SerializerMethodField
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import status
from rest_framework.exceptions import ValidationError
import base64 

from django.core.files.base import ContentFile

User = get_user_model()

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')  
            ext = format.split('/')[-1]  
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)

class UserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)
    avatar = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar'
        )

    def get_is_subscribed(self, creator):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Subscribtion.objects.filter(creator=creator, subscriber=request.user).exists()
    

class CreateUserSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя
    без проверки на подписку """

    class Meta:
        """Мета-параметры сериализатора"""

        model = User
        fields = (
            'email', 
            'id', 
            'username', 
            'first_name',
            'last_name', 
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    ingredients = RecipeIngredientSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, recipe):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favourite.objects.filter(user=request.user, recipe=recipe).exists()
    
    def get_is_in_shopping_cart(self, recipe):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return ShoppingList.objects.filter(user=request.user, recipe=recipe).exists()
    

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class ShoppingListSerialiser(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList


    
class SubscribtionSerializer(serializers.ModelSerializer):
    class Mets:
        model = User
        fields= (
            'email'
        )