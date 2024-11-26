from django.db import models
from django.utils.html import mark_safe

from django.db import models


from django.core.exceptions import ValidationError


class Ingredient(models.Model):
    MEASUREMENT_SCALE = [
        ('g', 'Граммы'),
        ('pcs', 'Штуки'),
        ('tbsp', 'Столовые ложки'),
        ('tsp', 'Чайные ложки'),
        ('ml', 'Миллилитры'),
    ]

    name = models.CharField(max_length=255, verbose_name="Название")
    image = models.ImageField(upload_to="images/", default="images/default.jpg", verbose_name="Изображение")

    unit = models.CharField(
        max_length=10,
        choices=MEASUREMENT_SCALE,
        default='g',
        verbose_name="Единица измерения",
    )
    conversion_to_grams = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Если ед. изм. штуки, то указать вес на 1 штуку в граммах",
        verbose_name="Вес шт/гр (опционально)",
    )

    calories = models.DecimalField(
        default=0.0,
        max_digits=6,
        decimal_places=2,
        help_text="Калорийность на 100 ед. изм.",
        verbose_name="Калорийность",
    )

    def clean(self):
        """Валидация данных модели."""
        if self.unit == 'pcs' and (self.conversion_to_grams is None or self.conversion_to_grams <= 0):
            raise ValidationError({
                'conversion_to_grams': "Для единицы измерения 'штуки' необходимо указать вес в граммах."
            })
        if self.unit != 'pcs' and self.conversion_to_grams:
            raise ValidationError({
                'conversion_to_grams': "Поле 'Вес шт/гр' должно быть пустым для выбранной единицы измерения."
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
