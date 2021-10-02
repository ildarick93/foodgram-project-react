from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import (CASCADE, CharField, ForeignKey, ImageField,
                              Model, PositiveIntegerField, SlugField,
                              TextField)
from django.db.models.fields.related import ManyToManyField

User = get_user_model()


class Tag(Model):
    name = CharField(max_length=200, unique=True, blank=False)
    color = CharField(max_length=7)
    slug = SlugField(max_length=200, unique=True, blank=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(Model):
    name = CharField(max_length=100, unique=True, db_index=True, blank=False)
    measurements_unit = CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.measurements_unit})'


class Recipe(Model):
    author = ForeignKey(User, on_delete=CASCADE, related_name='recipes')
    ingredients = ManyToManyField(
        Ingredient,
        through='IngredientAmountInRecipe',
        related_name='recipes'
    )
    tags = ManyToManyField(
        Tag,
        through='RecipeTags',
        related_name='recipes')
    image = ImageField(blank=False)
    name = CharField(max_length=200, unique=True, blank=False)
    text = TextField(blank=False)
    cooking_time = PositiveIntegerField(
        validators=[MinValueValidator(1, 'Cooking time must be > 0')]
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class IngredientAmountInRecipe(Model):
    ingredient = ForeignKey(Ingredient, on_delete=CASCADE)
    recipe = ForeignKey(Recipe, on_delete=CASCADE)
    amount = PositiveIntegerField(
        validators=[
            MinValueValidator(1, 'Ingredient amount must be > 0')]
    )

    class Meta:
        ordering = ['recipe']
        unique_together = ['ingredient', 'recipe']

    def __str__(self):
        return f'Need {self.amount} of {self.ingredient} for {self.recipe}'


class RecipeTags(Model):
    recipe = ForeignKey(Recipe, on_delete=CASCADE)
    tag = ForeignKey(Tag, on_delete=CASCADE)

    class Meta:
        ordering = ['recipe']
        unique_together = ['tag', 'recipe']

    def __str__(self):
        return f'Pair of {self.tag}, {self.recipe}'


class FavoriteRecipe(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='favorite_recipes'
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='is_favorite_for_users',
    )

    class Meta:
        unique_together = ['user', 'recipe']

    def __str__(self):
        return f'{self.user} likes {self.recipe}'


class ShoppingList(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='recipes_in_shopping_list'
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='is_in_shopping_list'
    )

    class Meta:
        unique_together = ['user', 'recipe']

    def __str__(self):
        return f'{self.recipe} is in shopping list of {self.user}'
