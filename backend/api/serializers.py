from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import CustomUserSerializer

from .models import (FavoriteRecipe, Ingredient, IngredientAmountInRecipe,
                     Recipe, RecipeTag, ShoppingList, Tag)

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = IngredientAmountInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    image = Base64ImageField()
    ingredient = IngredientAmountInRecipeSerializer(
        source='ingredient_amount',
        many=True
    )
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('text', 'author', 'ingredient', 'tags', 'image', 'name',
                  'id', 'cooking_time', 'is_favorited', 'is_in_shopping_cart')

    def _is_in_list(self, model, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        if model.objects.filter(
            recipe=obj,
            user=self.context['request'].user
        ).exists():
            return True
        return False

    def get_is_favorited(self, obj):
        return self._is_in_list(FavoriteRecipe, obj)

    def get_is_in_shopping_cart(self, obj):
        return self._is_in_list(ShoppingList, obj)

    def create_tags(self, tags, recipe):
        for tag_id in tags:
            tag = get_object_or_404(Tag, id=tag_id)
            RecipeTag.objects.create(tag=tag, recipe=recipe)

    def update_tags(self, tags, recipe):
        RecipeTag.objects.filter(recipe=recipe).delete()
        self.create_tags(tags, recipe)

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_id, amount = ingredient['id'], ingredient['amount']
            ingredient_obj = get_object_or_404(Ingredient, id=ingredient_id)
            IngredientAmountInRecipe.objects.create(
                ingredient=ingredient_obj,
                amount=amount,
                recipe=recipe
            )

    def update_ingredients(self, ingredients, recipe):
        IngredientAmountInRecipe.objects.filter(recipe=recipe).delete()
        self.create_ingredients(ingredients, recipe)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredient_amount')

        recipe = Recipe.objects.create(**validated_data)

        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', False)
        ingredients = validated_data.pop('ingredient_amount', False)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if tags:
            self.update_tags(tags, instance)
        if ingredients:
            self.update_ingredients(ingredients, instance)

        return instance


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')


class ShoppingListSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='recipe.name')
    image = Base64ImageField(source='recipe.image')
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = ShoppingList
        fields = ('id', 'name', 'image', 'cooking_time')
