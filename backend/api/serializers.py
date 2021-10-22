from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.serializers import CustomUserSerializer

from .models import (FavoriteRecipe, Ingredient, IngredientAmountInRecipe,
                     Recipe, RecipeTag, ShoppingList, Tag)

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


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
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmountInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientToRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmountInRecipe
        fields = ('id', 'amount')


class CreateUpdateRecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    ingredients = AddIngredientToRecipeSerializer(many=True)
    image = Base64ImageField()
    name = serializers.CharField(required=False)
    text = serializers.CharField(required=False)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('__all__')

    def validate_cooking_time(self, data):
        if data <= 0:
            raise ValidationError('Cooking time must be > 0')
        return data

    def validate_tags(self, data):
        tags = self.initial_data.get('tags')
        if len(tags) == 0:
            raise serializers.ValidationError('Add at least 1 tag')
        return data

    def validate_ingredients(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise ValidationError('You have to select at least 1 ingredient')
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise ValidationError('Ingredient amount must be > 0')
        return data

    def create_tags(self, tags, recipe):
        for tag in tags:
            RecipeTag.objects.create(recipe=recipe, tag=tag)

    def update_tags(self, tags, recipe):
        RecipeTag.objects.filter(recipe=recipe).delete()
        self.create_tags(tags, recipe)

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            IngredientAmountInRecipe.objects.create(
                ingredient=ingredient_id,
                amount=amount,  # ingredient.get('amount')
                recipe=recipe
            )

    def update_ingredients(self, ingredients, recipe):
        IngredientAmountInRecipe.objects.filter(recipe=recipe).delete()
        self.create_ingredients(ingredients, recipe)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', False)
        ingredients = validated_data.pop('ingredients', False)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags:
            self.update_tags(tags, instance)
        if ingredients:
            self.update_ingredients(ingredients, instance)
        return instance


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    image = Base64ImageField()
    ingredients = IngredientAmountInRecipeSerializer(
        source='ingredients_amount',
        many=True
    )
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('text', 'author', 'ingredients', 'tags', 'image', 'name',
                  'id', 'cooking_time', 'is_favorited', 'is_in_shopping_cart')

    def _is_in_list(self, model, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        return model.objects.filter(
            recipe=obj,
            user=self.context['request'].user
        ).exists()

    def get_is_favorited(self, obj):
        return self._is_in_list(FavoriteRecipe, obj)

    def get_is_in_shopping_cart(self, obj):
        return self._is_in_list(ShoppingList, obj)


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
