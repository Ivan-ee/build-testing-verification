from django.db import models
from django.utils.html import mark_safe


# Create your models here.

class Ingredient(models.Model):
    """Составная часть рецепта."""
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/", default="images/default.jpg", )
    calories = models.DecimalField(default=0.0, max_digits=6, decimal_places=2,
                                   help_text="Калорийность в ккал на 100 грамм")

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Вкусное делается по рецепту."""
    name = models.CharField(max_length=300)
    description = models.TextField(default="", help_text="Описание")
    cooking_time = models.IntegerField(default=0)
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")

    def total_weight(self):
        return sum(ri.weight for ri in self.recipeingredient_set.all())

    def total_calories(self):
        total_calories = sum(
            (ri.weight / 100) * ri.ingredient.calories for ri in self.recipeingredient_set.all()
        )
        return round(total_calories, 2)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Один ингредиент может быть
    в нескольких рецептах,
    как и в одном рецепте может быть
    несколько ингредиентов."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    weight = models.DecimalField(default=0.0, max_digits=6, decimal_places=1, help_text="Вес в граммах")

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name} ({self.weight} г)'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique recipes ingredients'
            )
        ]
