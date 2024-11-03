from django.db import models


# Create your models here.

class Ingredient(models.Model):
    """Составная часть рецепта."""
    name = models.CharField(max_length=255)


class Recipe(models.Model):
    """Вкусное делается по рецепту."""
    name = models.CharField(max_length=300)
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")


class RecipeIngredient(models.Model):
    """Один ингредиент может быть
    в нескольких рецептах,
    как и в одном рецепте может быть
    несколько ингредиентов."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
