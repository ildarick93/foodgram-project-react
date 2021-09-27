from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .serializers import CustomUserCreateSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserCreateSerializer
    lookup_field = 'username'
