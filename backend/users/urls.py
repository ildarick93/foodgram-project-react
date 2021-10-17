# from django.conf.urls import include
# from django.urls import path
from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

router = DefaultRouter()

router.register('users', CustomUserViewSet)

User = get_user_model()

urlpatterns = router.urls
# urlpatterns = [
#     path('', include('djoser.urls')),
#     path('auth/', include('djoser.urls.authtoken')),
# ]
