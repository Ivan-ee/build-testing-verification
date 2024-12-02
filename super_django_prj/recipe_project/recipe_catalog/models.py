from django.db import models
from django.utils.html import mark_safe

from django.db import models

from django.core.exceptions import ValidationError


class MeasurementScale(models.Model):
    label = models.CharField(max_length=50, verbose_name="Единица измерения")
    key = models.CharField(max_length=10, unique=True, verbose_name="Сокращение")
    abbreviation = models.TextField(default="")

    def __str__(self):
        return self.label


class VolumeUnitConversion(models.Model):
    unit = models.ForeignKey(
        MeasurementScale,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    weight = models.IntegerField()


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
                'weight_by_pcs': "Для единицы измерения 'штуки' необходимо указать вес в граммах"
            })
        if self.unit and self.unit.key != self.PCS and self.weight_by_pcs:
            raise ValidationError({
                'weight_by_pcs': "Поле 'Вес шт/гр' должно быть пустым для выбранной единицы измерения"
            })

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(default="", help_text="Описание")
    image = models.ImageField(upload_to="images/", default="images/default.jpg", verbose_name="Изображение")
    cooking_time = models.IntegerField(default=0)
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")

    def total_weight(self):
        total_weight = 0
        for ri in self.recipeingredient_set.all():
            ingredient = ri.ingredient
            if ingredient.unit.key == ingredient.PCS:
                weight_in_grams = ri.count * ingredient.weight_by_pcs
            else:
                if ingredient.unit:
                    volume_conversion = VolumeUnitConversion.objects.filter(unit=ingredient.unit).first()
                    if volume_conversion:
                        weight_in_grams = ri.count * volume_conversion.weight
                    else:
                        weight_in_grams = ri.count
                else:
                    weight_in_grams = ri.count

            total_weight += weight_in_grams
        return total_weight

    def total_calories(self):
        """Общая калорийность рецепта."""
        total_calories = 0
        for ri in self.recipeingredient_set.all():
            ingredient = ri.ingredient
            if ingredient.unit and ingredient.unit.key == ingredient.PCS:
                weight_in_grams = ri.count * ingredient.weight_by_pcs
            elif ingredient.unit:
                volume_conversion = VolumeUnitConversion.objects.filter(unit=ingredient.unit).first()
                if volume_conversion:
                    weight_in_grams = ri.count * volume_conversion.weight
                else:
                    weight_in_grams = ri.count
            else:
                weight_in_grams = ri.count

            calories = (weight_in_grams / 100) * ingredient.calories
            total_calories += calories

        return round(total_calories, 2)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Один ингредиент может быть в нескольких рецептах,
    как и в одном рецепте может быть несколько ингредиентов."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def get_help_text(self):
        return "Количество в граммах"

    count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name} ({self.count} г)'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique recipes ingredients'
            )
        ]
