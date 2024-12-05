from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Recipe, Ingredient, RecipeIngredient, MeasurementScale
from django.conf import settings


class RecipeCatalogViewsTests(TestCase):
    HOME_URL = reverse('recipe_catalog:home')
    HOME_TEMPLATE = 'recipe_catalog/index.html'

    DETAILS_URL = 'recipe_catalog:detail'
    DETAILS_TEMPLATE = 'recipe_catalog/recipe.html'

    ABOUT_URL = reverse('recipe_catalog:about')
    ABOUT_TEMPLATE = 'recipe_catalog/about.html'

    USER_NAME = "testuser"

    MS_LABEL_1 = "Граммы"
    MS_KEY_1 = "g"
    MS_ABR_1 = "г"

    INGREDIENT_RECIPE_1 = ["Яблоко", "Морковь", "Груша", "Рис"]
    INGREDIENT_RECIPE_2 = ["Перец", "Картофель", "Сахар"]
    INGREDIENT_RECIPE_3 = ["Сливки"]

    RECIPE_NAME_1 = "Шарлотка"
    RECIPE_NAME_2 = "Борщ"
    RECIPE_NAME_3 = "Йогурт"

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username=cls.USER_NAME)

        cls.ms = MeasurementScale.objects.create(
            label=cls.MS_LABEL_1, key=cls.MS_KEY_1, abbreviation=cls.MS_ABR_1
        )

        cls.ingredients_recipe_1 = [
            Ingredient.objects.create(name=name, calories=50)
            for name in cls.INGREDIENT_RECIPE_1
        ]

        cls.ingredients_recipe_2 = [
            Ingredient.objects.create(name=name, calories=200)
            for name in cls.INGREDIENT_RECIPE_2
        ]

        cls.ingredients_recipe_3 = [
            Ingredient.objects.create(name=name, calories=200)
            for name in cls.INGREDIENT_RECIPE_3
        ]

        cls.recipe_1 = Recipe.objects.create(name=cls.RECIPE_NAME_1, description="Тестовое описание", author=cls.user)

        cls.recipe_2 = Recipe.objects.create(name=cls.RECIPE_NAME_2, description="Тестовое описание", author=cls.user)

        cls.recipe_3 = Recipe.objects.create(name=cls.RECIPE_NAME_3, description="Тестовое описание", author=cls.user)

        for ingredient in cls.ingredients_recipe_1:
            RecipeIngredient.objects.create(recipe=cls.recipe_1, ingredient=ingredient, unit=cls.ms, count=100)

        for ingredient in cls.ingredients_recipe_2:
            RecipeIngredient.objects.create(recipe=cls.recipe_2, ingredient=ingredient, unit=cls.ms, count=30)

        for ingredient in cls.ingredients_recipe_3:
            RecipeIngredient.objects.create(recipe=cls.recipe_3, ingredient=ingredient, unit=cls.ms, count=200)

    def test_index_view(self):
        """Отображение главной страницы"""
        response = self.client.get(self.HOME_URL)

        with self.subTest("Проверка шаблона"):
            self.assertTemplateUsed(response, self.HOME_TEMPLATE)

        recipes = response.context['recipes']

        recipe_names = [recipe.name for recipe in recipes]

        with self.subTest("Проверка алфавитного порядка рецептов"):
            self.assertEqual(recipe_names, sorted(recipe_names))

    def test_index_view_recipe_count_limit(self):
        """Отображение рецептов на главной странице с ограничением по количеству"""
        for i in range(11):
            Recipe.objects.create(name=f"Рецепт {i}", description="Тестовый рецепт", author=self.user)

        response = self.client.get(self.HOME_URL)

        recipes = response.context['recipes']
        self.assertLessEqual(len(recipes), settings.OBJS_ON_PAGE)

    def test_details_view(self):
        """Отображение страницы рецепта"""
        recipe = self.recipe_1
        response = self.client.get(reverse(self.DETAILS_URL, args=[recipe.pk]))

        with self.subTest("Проверка шаблона"):
            self.assertTemplateUsed(response, self.DETAILS_TEMPLATE)

        context = response.context
        expected_values = {
            "title": recipe.name,
            "description": recipe.description,
            "cooking_time": recipe.cooking_time,
            "total_weight": recipe.total_weight(),
            "total_calories": recipe.total_calories(),
        }

        for key, expected_value in expected_values.items():
            with self.subTest(f"Проверка значения {key}"):
                self.assertEqual(context[key], expected_value)

        ingredients_from_context = context['ingredients']
        ingredient_names = [ingredient['name'] for ingredient in ingredients_from_context]

        with self.subTest("Проверка количества ингредиентов"):
            self.assertEqual(len(ingredient_names), len(self.INGREDIENT_RECIPE_1))

        with self.subTest("Проверка сортировки ингредиентов"):
            self.assertEqual(ingredient_names, sorted(self.INGREDIENT_RECIPE_1))

    def test_about_view(self):
        """Страница о нас"""
        response = self.client.get(self.ABOUT_URL)
        self.assertTemplateUsed(response, self.ABOUT_TEMPLATE)
