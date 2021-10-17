from django.conf.urls import include
from django.contrib.auth import get_user_model
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

router = DefaultRouter()

router.register('users', CustomUserViewSet)

User = get_user_model()

urlpatterns = [
    path('', include(router.urls)),
]
