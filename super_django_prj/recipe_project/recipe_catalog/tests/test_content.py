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

    INGREDIENT_NAMES = ["Яблоко", "Морковь", "Груша", "Перец", "Картофель", "Сахар"]
    RECIPE_NAMES = ["Шарлотка", "Салат Цезарь", "Оливье", "Суп Харчо", "Борщ", "Блинчики"]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username=cls.USER_NAME)

        cls.ms = MeasurementScale.objects.create(
            label=cls.MS_LABEL_1, key=cls.MS_KEY_1, abbreviation=cls.MS_ABR_1
        )

        cls.ingredients = [
            Ingredient.objects.create(name=name, calories=50)
            for name in cls.INGREDIENT_NAMES
        ]

        cls.recipes = [
            Recipe.objects.create(name=name, description="Тестовое описание", author=cls.user)
            for name in cls.RECIPE_NAMES
        ]

        for ingredient in reversed(cls.ingredients):
            RecipeIngredient.objects.create(recipe=cls.recipes[0], ingredient=ingredient, unit=cls.ms, count=100)

    def test_index_view(self):
        """Отображение главной страницы"""
        response = self.client.get(self.HOME_URL)

        with self.subTest("Проверка шаблона"):
            self.assertTemplateUsed(response, self.HOME_TEMPLATE)

        expected_recipes = sorted(self.RECIPE_NAMES)
        recipes = [recipe.name for recipe in response.context['recipes']]

        for expected, actual in zip(expected_recipes, recipes):
            with self.subTest(f"Проверка вывода рецепта в алфавитном порядке {expected}"):
                self.assertEqual(actual, expected)

    def test_index_view_recipe_count_limit(self):
        """Отображение рецептов на главной странице с ограничением по количеству"""
        for i in range(11):
            Recipe.objects.create(name=f"Рецепт {i}", description="Тестовый рецепт", author=self.user)

        response = self.client.get(self.HOME_URL)

        recipes = response.context['recipes']
        self.assertLessEqual(len(recipes), settings.OBJS_ON_PAGE)

    def test_details_view(self):
        """Отображение страницы рецепта"""
        recipe = self.recipes[0]
        response = self.client.get(reverse(self.DETAILS_URL, args=[recipe.pk]))

        with self.subTest("Проверка шаблона"):
            self.assertTemplateUsed(response, self.DETAILS_TEMPLATE)

        context = response.context

        checks = {
            "title": context['title'],
            "description": context['description'],
            "cooking_time": context['cooking_time'],
            "total_weight": context['total_weight'],
            "total_calories": context['total_calories'],
        }

        expected_values = {
            "title": recipe.name,
            "description": recipe.description,
            "cooking_time": recipe.cooking_time,
            "total_weight": recipe.total_weight(),
            "total_calories": recipe.total_calories(),
        }

        for key, actual in checks.items():
            with self.subTest(f"Проверка {key}"):
                self.assertEqual(actual, expected_values[key])

        with self.subTest("Проверка количества ингредиентов"):
            self.assertEqual(len(context['ingredients']), len(self.INGREDIENT_NAMES))

    def test_ingredients_sorted_details_view(self):
        """Ингредиенты на странице рецепта выводятся по алфавиту"""
        response = self.client.get(reverse(self.DETAILS_URL, args=[self.recipes[0].pk]))

        ingredients_from_context = response.context['ingredients']

        self.assertEqual(
            [ingredient['name'] for ingredient in ingredients_from_context],
            sorted(self.INGREDIENT_NAMES)
        )

    def test_about_view(self):
        """Страница о нас"""
        response = self.client.get(self.ABOUT_URL)
        self.assertTemplateUsed(response, self.ABOUT_TEMPLATE)
