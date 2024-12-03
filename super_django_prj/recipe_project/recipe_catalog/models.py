from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User

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
    name = models.CharField(max_length=255, verbose_name="Название")

    calories = models.IntegerField(
        default=0,
        help_text="Калорийность на 100 ед. изм.",
        verbose_name="Калорийность",
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    PCS = "pcs"
    G = "g"
    ML = "ml"

    name = models.CharField(max_length=300, verbose_name="Название блюда")
    description = models.TextField(default="", verbose_name="Описание")
    image = models.ImageField(upload_to="images/", default="images/default.jpg", verbose_name="Изображение")
    cooking_time = models.IntegerField(default=0, verbose_name="Время приготовления",
                                       help_text="Время приготовления в минутах")
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes", verbose_name="Автор")

    def total_weight(self):
        """Общий вес рецепта в граммах."""
        total_weight = 0
        for ri in self.recipeingredient_set.all():
            if ri.unit and ri.unit.key == self.PCS:
                weight = ri.count * ri.weight_by_pcs
            elif ri.unit and ri.unit.key in [self.G, self.ML]:
                weight = ri.count
            elif ri.unit:
                conversion = VolumeUnitConversion.objects.filter(unit=ri.unit).first()
                weight = ri.count * (conversion.weight if conversion else 0)
            else:
                weight = ri.count
            total_weight += weight
        return total_weight

    def total_calories(self):
        """Общая калорийность рецепта."""
        total_calories = 0

        for ri in self.recipeingredient_set.all():
            if ri.unit and ri.unit.key == self.PCS:
                weight_in_grams = ri.count * (ri.weight_by_pcs or 0)
            elif ri.unit and ri.unit.key in [self.G, self.ML]:
                weight_in_grams = ri.count
            elif ri.unit:
                conversion = VolumeUnitConversion.objects.filter(unit=ri.unit).first()
                weight_in_grams = ri.count * (conversion.weight if conversion else 0)
            else:
                weight_in_grams = ri.count

            total_calories += (weight_in_grams / 100) * ri.ingredient.calories

        return round(total_calories, 2)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Один ингредиент может быть в нескольких рецептах,
    как и в одном рецепте может быть несколько ингредиентов."""

    PCS = "pcs"

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Ингредиент")
    unit = models.ForeignKey(
        MeasurementScale,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Выберите в чем измеряется ингредиент (граммы, штуки, миллилитры, ложки)",
        verbose_name="Единица измерения",
    )

    weight_by_pcs = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Если ед. изм. штуки, то указать вес на 1 штуку в граммах",
        verbose_name="Вес шт/гр (опционально)",
    )

    count = models.IntegerField(
        default=0,
        verbose_name="Количество",
        help_text="Количество выбранного ингредиента"
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

    def get_help_text(self):
        return "Количество в граммах"

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique recipes ingredients'
            )
        ]
