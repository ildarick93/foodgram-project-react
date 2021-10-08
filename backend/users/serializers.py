from api.models import Recipe
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        fields = tuple(User.REQUIRED_FIELDS) + (
            'username',
            'email',
            'password',
            'first_name',
            'last_name')


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.subscribers.filter(subscriber=request.user).exists()


class RecipeLiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionsSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes',
                  'recipes_count')

    def get_recipes(self, obj):
        query_params = self.context['request'].query_params
        recipes_limit = query_params.get('recipes_limit', False)
        if recipes_limit:
            recipes_limit = int(recipes_limit)
            recipes = Recipe.objects.filter(author=obj)[:recipes_limit]
        else:
            recipes = Recipe.objects.filter(author=obj)
        serializer = RecipeLiteSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
