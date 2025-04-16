# urls.py
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, IngredientsViewSet, RecipesViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
] 