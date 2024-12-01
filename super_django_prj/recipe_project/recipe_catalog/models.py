from django.db import models
from django.utils.html import mark_safe

from django.db import models


from django.core.exceptions import ValidationError


class MeasurementScale(models.Model):
    label = models.CharField(max_length=50, verbose_name="Единица измерения")
    key = models.CharField(max_length=10, unique=True, verbose_name="Сокращение")

    def __str__(self):
        return self.label


class Ingredient(models.Model):
    PCS = 'pcs'

    name = models.CharField(max_length=255, verbose_name="Название")

    unit = models.ForeignKey(
        MeasurementScale,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Единица измерения",
    )

    weight_by_pcs = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Если ед. изм. штуки, то указать вес на 1 штуку в граммах",
        verbose_name="Вес шт/гр (опционально)",
    )

    calories = models.IntegerField(
        default=0,
        help_text="Калорийность на 100 ед. изм.",
        verbose_name="Калорийность",
    )

    def clean(self):
        """Валидация данных модели."""
        if self.unit and self.unit.key == self.PCS and (self.weight_by_pcs is None or self.weight_by_pcs <= 0):
            raise ValidationError({
                'weight_by_pcs': "Для единицы измерения 'штуки' необходимо указать вес в граммах."
            })
        if self.unit and self.unit.key != self.PCS and self.weight_by_pcs:
            raise ValidationError({
                'weight_by_pcs': "Поле 'Вес шт/гр' должно быть пустым для выбранной единицы измерения."
            })

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(default="", help_text="Описание")
    cooking_time = models.IntegerField(default=0)
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")

    def total_weight(self):
        return sum(
            ri.weight * ri.ingredient.conversion_to_grams
            for ri in self.recipeingredient_set.all()
        )

    def total_calories(self):
        total_calories = sum(
            (ri.weight * ri.ingredient.conversion_to_grams / 100) * ri.ingredient.calories
            for ri in self.recipeingredient_set.all()
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
