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
        cls.user = User.objects.create(username="test_user")

        cls.recipe1 = Recipe.objects.create(name="рецепт 1", author=cls.user)
        cls.recipe2 = Recipe.objects.create(name="рецепт 2", author=cls.user)

        cls.ingredient1 = Ingredient.objects.create(name="Сахар", calories=400)
        cls.ingredient2 = Ingredient.objects.create(name="Мука", calories=350)
        cls.ingredient3 = Ingredient.objects.create(name="Рис", calories=200)

        MeasurementScale.objects.all().delete()
        cls.unit_grams = MeasurementScale.objects.create(label="граммы", key="g", abbreviation="г")
        cls.unit_pcs = MeasurementScale.objects.create(label="штуки", key="pcs", abbreviation="шт")
        cls.unit_tsp = MeasurementScale.objects.create(label="чайная ложка", key="tsp", abbreviation="ч.л")
        cls.unit_tbsp = MeasurementScale.objects.create(label="столовая ложка", key="tbsp", abbreviation="ст.л")

        VolumeUnitConversion.objects.create(unit=cls.unit_tsp, weight=5)
        VolumeUnitConversion.objects.create(unit=cls.unit_tbsp, weight=15)

        cls.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=cls.recipe1,
            ingredient=cls.ingredient1,
            unit=cls.unit_pcs,
            count=3,
            weight_by_pcs=50
        )

    def test_ingredient_creation(self):
        self.assertEqual(self.recipe_ingredient.recipe.name, self.recipe1.name)

    def test_weight_calculation_with_pcs(self):
        self.assertEqual(self.recipe_ingredient.recipe.total_weight(), 150)

    def test_weight_calculation_with_tsp(self):
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe2,
            ingredient=self.ingredient1,
            unit=self.unit_tsp,
            count=4
        )
        self.assertEqual(recipe_ingredient.recipe.total_weight(), 20)

    def test_weight_calculation_with_tbsp(self):
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe2,
            ingredient=self.ingredient1,
            unit=self.unit_tbsp,
            count=3
        )
        self.assertEqual(recipe_ingredient.recipe.total_weight(), 45)

    def test_combined_weight_calculation(self):
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe2,
            ingredient=self.ingredient1,
            unit=self.unit_grams,
            count=200
        )
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe2,
            ingredient=self.ingredient2,
            unit=self.unit_pcs,
            count=3,
            weight_by_pcs=50
        )
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe2,
            ingredient=self.ingredient3,
            unit=self.unit_tsp,
            count=4
        )
        self.assertEqual(recipe_ingredient.recipe.total_weight(), 370)

    def test_unique_constraint(self):
        RecipeIngredient.objects.create(recipe=self.recipe2, ingredient=self.ingredient1, unit=self.unit_pcs, count=2)
        with self.assertRaises(IntegrityError):
            RecipeIngredient.objects.create(recipe=self.recipe2, ingredient=self.ingredient1, unit=self.unit_pcs,
                                            count=1)
