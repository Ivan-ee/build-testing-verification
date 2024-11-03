from django.db import models
from django.utils.html import mark_safe


# Create your models here.

class Ingredient(models.Model):
    """Составная часть рецепта."""
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/", default="images/default.jpg", )
    weight = models.DecimalField(default=0.0, max_digits=6, decimal_places=1, help_text="Вес в граммах")
    calories = models.DecimalField(default=0.0, max_digits=6, decimal_places=2,
                                   help_text="Калорийность в ккал на 100 грамм")

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Вкусное делается по рецепту."""
    name = models.CharField(max_length=300)
    cooking_time = models.IntegerField(default=0)
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")
    weight = models.DecimalField(default=0.0, max_digits=6, decimal_places=1, help_text="Вес в граммах")
    servings = models.IntegerField(default=2, help_text="Количество порций (по умолчанию 2)")

    def calculate_total_weight(self):
        """Calculate the total weight of the recipe based on ingredient weights."""
        total_weight = sum(
            recipe_ingredient.ingredient.weight for recipe_ingredient in self.recipeingredient_set.all()
        )
        self.weight = total_weight
        self.save()
        return total_weight

    def adjust_ingredients_for_servings(self, target_servings):
        """Adjust ingredient quantities for the target number of servings."""
        factor = target_servings / self.servings
        for recipe_ingredient in self.recipeingredient_set.all():
            recipe_ingredient.ingredient.weight *= factor
            recipe_ingredient.ingredient.save()
        self.servings = target_servings
        self.calculate_total_weight()
        self.save()

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Один ингредиент может быть
    в нескольких рецептах,
    как и в одном рецепте может быть
    несколько ингредиентов."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique recipes ingredients'
            )
        ]
