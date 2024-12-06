from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ..models import MeasurementScale, VolumeUnitConversion, Ingredient, Recipe, RecipeIngredient, User


class TestMeasurementScaleModel(TestCase):
    def test_measurement_scale_creation(self):
        scale = MeasurementScale.objects.create(label="граммы", key="g", abbreviation="гр.")
        self.assertEqual(scale.label, "граммы")
        self.assertEqual(scale.key, "g")
        self.assertEqual(scale.abbreviation, "гр.")


class TestVolumeUnitConversionModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.scale = MeasurementScale.objects.create(label="стакан", key="cup", abbreviation="ст.")

    def test_volume_unit_conversion_creation(self):
        conversion = VolumeUnitConversion.objects.create(unit=self.scale, weight=250)
        self.assertEqual(conversion.unit, self.scale)
        self.assertEqual(conversion.weight, 250)


class TestIngredientModel(TestCase):
    def test_ingredient_creation(self):
        ingredient = Ingredient.objects.create(name="Мука", calories=350)
        self.assertEqual(ingredient.name, "Мука")
        self.assertEqual(ingredient.calories, 350)


class TestRecipeModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username="test_user")
        cls.recipe = Recipe.objects.create(
            name="Блины",
            description="Традиционные русские блины.",
            cooking_time=30,
            author=cls.author,
        )
        cls.ingredient1 = Ingredient.objects.create(name="Мука", calories=350)
        cls.ingredient2 = Ingredient.objects.create(name="Молоко", calories=50)
        cls.scale = MeasurementScale.objects.create(label="граммы", key="g", abbreviation="гр.")

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.name, "Блины")
        self.assertEqual(self.recipe.author, self.author)
        self.assertEqual(self.recipe.description, "Традиционные русские блины.")
        self.assertEqual(self.recipe.cooking_time, 30)

    def test_total_weight_calculation(self):
        RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredient1, unit=self.scale, count=200)
        RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredient2, unit=self.scale, count=500)
        self.assertEqual(self.recipe.total_weight(), 700)

    def test_total_calories_calculation(self):
        RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredient1, unit=self.scale, count=200)
        RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredient2, unit=self.scale, count=500)
        self.assertEqual(self.recipe.total_calories(), 300)


class TestRecipeIngredientModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.recipe = Recipe.objects.create(name="Пирог", author=User.objects.create(username="test_user"))
        cls.ingredient = Ingredient.objects.create(name="Сахар", calories=400)
        cls.unit = MeasurementScale.objects.create(label="штуки", key="pcs", abbreviation="шт.")

    def test_recipe_ingredient_creation(self):
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            unit=self.unit,
            count=2,
            weight_by_pcs=50
        )
        self.assertEqual(recipe_ingredient.recipe, self.recipe)
        self.assertEqual(recipe_ingredient.ingredient, self.ingredient)
        self.assertEqual(recipe_ingredient.unit, self.unit)
        self.assertEqual(recipe_ingredient.count, 2)
        self.assertEqual(recipe_ingredient.weight_by_pcs, 50)

    def test_validation_error_weight_by_pcs_missing(self):
        recipe_ingredient = RecipeIngredient(
            recipe=self.recipe,
            ingredient=self.ingredient,
            unit=self.unit,
            count=2,
            weight_by_pcs=None
        )
        with self.assertRaises(ValidationError):
            recipe_ingredient.clean()

    def test_unique_constraint(self):
        RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredient, unit=self.unit, count=2)
        with self.assertRaises(IntegrityError):
            RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredient, unit=self.unit, count=1)
