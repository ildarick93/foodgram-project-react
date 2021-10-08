from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import (CASCADE, CharField, DateTimeField, ForeignKey,
                              ImageField, Model, PositiveIntegerField,
                              SlugField, TextField, UniqueConstraint)
from django.db.models.fields.related import ManyToManyField

User = get_user_model()


class Tag(Model):
    name = CharField(max_length=200, unique=True, verbose_name='Name of tag')
    color = CharField(max_length=7, verbose_name='Color of tag',)
    slug = SlugField(max_length=200, unique=True, verbose_name='Slug')

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Ingredient(Model):
    name = CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name='Name of ingredient'
    )
    measurements_unit = CharField(
        max_length=200,
        verbose_name='Unit of measurement'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return f'{self.name} ({self.measurements_unit})'


class Recipe(Model):
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='recipes',
        verbose_name='Author of recipe'
    )
    ingredients = ManyToManyField(
        Ingredient,
        through='IngredientAmountInRecipe',
        related_name='recipes',
        verbose_name='Ingredients'
    )
    tags = ManyToManyField(
        Tag,
        through='RecipeTag',
        related_name='recipes',
        verbose_name='Tag of recipe'
    )
    image = ImageField(upload_to='images/', verbose_name='Image of recipe')
    name = CharField(
        max_length=200,
        unique=True,
        verbose_name='Name of recipe'
    )
    text = TextField(verbose_name='Text of recipe')
    cooking_time = PositiveIntegerField(
        validators=[MinValueValidator(1, 'Cooking time must be > 0')],
        verbose_name='Required time for cooking the dish'
    )
    pub_date = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.name


class IngredientAmountInRecipe(Model):
    ingredient = ForeignKey(
        Ingredient,
        on_delete=CASCADE,
        verbose_name='Name of ingredient'
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Name of recipe'
    )
    amount = PositiveIntegerField(
        validators=[MinValueValidator(1, 'Ingredient amount must be > 0')],
        verbose_name='Amount of ingredient',
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Ingredient amount in recipe'
        verbose_name_plural = 'Ingredients amount in recipe'
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe'
            )
        ]

    def __str__(self):
        return f'Need {self.amount} of {self.ingredient} for {self.recipe}'


class RecipeTag(Model):
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Name of recipe'
    )
    tag = ForeignKey(Tag, on_delete=CASCADE, verbose_name='Tag of recipe')

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Tag of recipe'
        verbose_name_plural = 'Tags of recipe'
        constraints = [
            UniqueConstraint(
                fields=['tag', 'recipe'],
                name='unique_tag_in_recipe'
            )
        ]

    def __str__(self):
        return f'Pair of {self.tag}, {self.recipe}'


class FavoriteRecipe(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='favorite_recipes',
        verbose_name='Username'
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='is_favorite_for_users',
        verbose_name='Name of recipe'
    )

    class Meta:
        verbose_name = 'Favorite recipes'
        unique_together = ['user', 'recipe']
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe_for_user'
            )
        ]

    def __str__(self):
        return f'{self.user} likes {self.recipe}'


class ShoppingList(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='recipes_in_shopping_list',
        verbose_name='Username'
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='is_in_shopping_list',
        verbose_name='Name of recipe'
    )

    class Meta:
        verbose_name = 'Shopping list'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_list_for_user'
            )
        ]

    def __str__(self):
        return f'{self.recipe} is in shopping list of {self.user}'
