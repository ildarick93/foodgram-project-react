# Generated by Django 3.0.5 on 2021-10-06 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20211003_2219'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RecipeTags',
            new_name='RecipeTag',
        ),
    ]
