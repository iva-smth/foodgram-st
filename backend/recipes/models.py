from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import (MinValueValidator, RegexValidator, )

User = get_user_model()

class Ingredient(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name= 'Название', 
        unique=True
    )
    measurement_unit = models.CharField(
        max_length=64, 
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = (['name'])
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name= 'Автор',
        related_name= 'authors_recipes',
        on_delete= models.CASCADE,
    )
    name = models.CharField(
        max_length=256,
        verbose_name= 'Название' 
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to= 'images/recipes'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipe_ingredients',
        verbose_name='Ингредиенты'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(1, message='Минимальное значение 1!'),
        ]
    )

    class Meta:
        ordering = (['name'])
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message='Минимальное значение 1!')],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe'
            )
        ]

    def __str__(self):
        return f"{self.amount} {self.ingredient.measurement_unit} of {self.ingredient.name}"
    

class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favourites',
        verbose_name='Пользователь',
        on_delete= models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favourites',
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ['user', 'recipe']

    def __str__(self):
        return f'{self.user} {self.recipe}'
    

class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        unique_together = ['user', 'recipe']

    def __str__(self):
        return f'{self.user} {self.recipe}'