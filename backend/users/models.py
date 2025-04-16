# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    first_name = models.CharField(max_length = 150, verbose_name = 'Имя')
    last_name = models.CharField(max_length = 150, verbose_name = 'Фамилия')
    username = models.CharField(max_length = 150, verbose_name = 'Логин', unique = True, validators=[
            RegexValidator(
                regex='^[\w.@+-]+$',
                message='Username is not valid',
            ),
        ])
    email = models.EmailField(max_length = 254, verbose_name = 'Электроная почта', unique = True)
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to= 'users/images',
        null=True,  
        default=None
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = (['id'])
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
    
class Subscribtion(models.Model):
    creator = models.ForeignKey(
        User, 
        verbose_name= 'Автор',
        related_name= 'subscription', 
        on_delete= models.CASCADE,
    )

    subscriber = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        related_name='subscribtion',
        on_delete=models.CASCADE,
    )
    
    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = [['creator', 'subscriber']]

    def __str__(self):
        return f'{self.subscriber} подписан на {self.creator}'
