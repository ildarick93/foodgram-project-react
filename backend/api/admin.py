from django.contrib import admin

from .models import (FavoriteRecipe, Ingredient, IngredientAmountInRecipe,
                     Recipe, RecipeTags, ShoppingList, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'text', 'cooking_time')
    search_fields = ('name', 'author')
    list_filter = ('name', 'author')


@admin.register(RecipeTags)
class RecipeTagsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'tag')
    search_fields = ('recipe', 'tag')
    list_filter = ('recipe', 'tag')


@admin.register(IngredientAmountInRecipe)
class IngredientAmountInRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe', 'ingredient')
    list_filter = ('recipe', 'ingredient')


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')


@admin.register(ShoppingList)
class ShoppingListAdmin(FavoriteRecipeAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
