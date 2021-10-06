# Generated by Django 3.0.5 on 2021-10-03 19:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinglist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes_in_shopping_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recipetags',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Recipe'),
        ),
        migrations.AddField(
            model_name='recipetags',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Tag'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='api.IngredientAmountInRecipe', to='api.Ingredient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', through='api.RecipeTags', to='api.Tag'),
        ),
        migrations.AddField(
            model_name='ingredientamountinrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Ingredient'),
        ),
        migrations.AddField(
            model_name='ingredientamountinrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Recipe'),
        ),
        migrations.AddField(
            model_name='favoriterecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_favorite_for_users', to='api.Recipe'),
        ),
        migrations.AddField(
            model_name='favoriterecipe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_recipes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='shoppinglist',
            unique_together={('user', 'recipe')},
        ),
        migrations.AlterUniqueTogether(
            name='recipetags',
            unique_together={('tag', 'recipe')},
        ),
        migrations.AlterUniqueTogether(
            name='ingredientamountinrecipe',
            unique_together={('ingredient', 'recipe')},
        ),
        migrations.AlterUniqueTogether(
            name='favoriterecipe',
            unique_together={('user', 'recipe')},
        ),
    ]
