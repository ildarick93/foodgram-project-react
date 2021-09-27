from djoser.serializers import UserCreateSerializer

from .models import CustomUser

# from rest_framework import serializers


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = (
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
        )

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
