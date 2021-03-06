from django.contrib.auth import get_user_model
from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.serializers import CustomUserSerializer

from .models import (FavoriteRecipe, Ingredient,  # RecipeTag,
                     IngredientAmountInRecipe, Recipe, ShoppingList, Tag)

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

    def create(self, validated_data):
        author = self.context.get('request').user
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.ingredients_recipe(ingredients_data, recipe)
        recipe.tags.set(tags_data)
        return recipe

    def ingredients_recipe(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            if IngredientAmountInRecipe.objects.filter(
                recipe=recipe, ingredient=ingredient_id
            ).exists():
                amount += F('amount')
            IngredientAmountInRecipe.objects.update_or_create(
                recipe=recipe, ingredient=ingredient_id,
                defaults={'amount': amount})

    def update(self, recipe, validated_data):
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.cooking_time = validated_data.get('cooking_time',
                                                 recipe.cooking_time)
        recipe.image = validated_data.get('image', recipe.image)
        if 'ingredients' in self.initial_data:
            ingredients = validated_data.pop('ingredients')
            recipe.ingredients.clear()
            self.ingredients_recipe(ingredients, recipe)
        if 'tags' in self.initial_data:
            tags_data = validated_data.pop('tags')
            recipe.tags.set(tags_data)
        recipe.save()
        return recipe

    def to_representation(self, recipe):
        return RecipeSerializer(
            recipe, context={'request':
                             self.context.get('request')}).data


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
