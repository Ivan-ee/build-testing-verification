from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db import IntegrityError, transaction
from ..models import MeasurementScale, VolumeUnitConversion, Ingredient, Recipe, RecipeIngredient, User


class TestMeasurementScaleModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.scale = MeasurementScale.objects.create(label="msl", key="msk", abbreviation="msabr")

    def test_measurement_scale_creation(self):
        self.assertEqual(self.scale.label, "msl")
        self.assertEqual(self.scale.key, "msk")
        self.assertEqual(self.scale.abbreviation, "msabr")

    def test_measurement_scale_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                MeasurementScale.objects.create(label="msl", key="msk2", abbreviation="msabr")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                MeasurementScale.objects.create(label="msl2", key="msk", abbreviation="msabr")


class TestVolumeUnitConversionModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.scale = MeasurementScale.objects.create(label="стакан", key="cup", abbreviation="ст.")
        cls.conversion = VolumeUnitConversion.objects.create(unit=cls.scale, weight=250)

    def test_volume_unit_conversion_creation(self):
        self.assertEqual(self.conversion.unit, self.scale)
        self.assertEqual(self.conversion.weight, 250)

    def test_volume_unit_conversion_with_none_scale(self):
        with self.assertRaises(IntegrityError):
            VolumeUnitConversion.objects.create(unit=None, weight=None)

    def test_volume_unit_conversion_unique(self):
        with self.assertRaises(IntegrityError):
            MeasurementScale.objects.create(label="стакан", key="cup", abbreviation="ст.")


class TestIngredientModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ingredient = Ingredient.objects.create(name="Мука", calories=350)

    def test_ingredient_creation(self):
        self.assertEqual(self.ingredient.name, "Мука")
        self.assertEqual(self.ingredient.calories, 350)

    def test_ingredient_unique(self):
        with self.assertRaises(IntegrityError):
            Ingredient.objects.create(name="Мука")

    def test_ingredient_without_name(self):
        ingredient = Ingredient.objects.create()

        self.assertEqual(ingredient.name, "Ингредиент")


class TestRecipeModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username="test_user")
        cls.recipe = Recipe.objects.create(
            name="Блины",
            description="Традиционные русские блины",
            cooking_time=30,
            author=cls.author,
        )
        cls.ingredient1 = Ingredient.objects.create(name="Мука", calories=350)
        cls.ingredient2 = Ingredient.objects.create(name="Молоко", calories=50)
        cls.scale = MeasurementScale.objects.get(key="g")

        RecipeIngredient.objects.create(recipe=cls.recipe, ingredient=cls.ingredient1, unit=cls.scale, count=200)
        RecipeIngredient.objects.create(recipe=cls.recipe, ingredient=cls.ingredient2, unit=cls.scale, count=500)

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.name, "Блины")
        self.assertEqual(self.recipe.author, self.author)
        self.assertEqual(self.recipe.description, "Традиционные русские блины")
        self.assertEqual(self.recipe.cooking_time, 30)

    def test_total_weight_calculation(self):
        self.assertEqual(self.recipe.total_weight(), 700)

    def test_total_calories_calculation(self):
        self.assertEqual(self.recipe.total_calories(), 950)

    def test_recipe_creation_with_duplicate_name(self):
        with self.assertRaises(IntegrityError):
            Recipe.objects.create(
                name="Блины",
                description="Те же самые блины",
                cooking_time=20,
                author=self.author,
            )

    def test_recipe_creation_without_author(self):
        with self.assertRaises(IntegrityError):
            Recipe.objects.create(
                name="Рецепт",
                description="Традиционные русские блины",
                cooking_time=30,
            )


class TestRecipeIngredientModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.recipe = Recipe.objects.create(name="Пирог", author=User.objects.create(username="test_user"))
        cls.ingredient = Ingredient.objects.create(name="Сахар", calories=400)
        cls.unit = MeasurementScale.objects.get(key="pcs")

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
