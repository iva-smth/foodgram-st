# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# Регистрируем модель в админке:
admin.site.register(User, UserAdmin)