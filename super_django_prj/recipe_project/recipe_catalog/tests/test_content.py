from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Recipe, Ingredient

User = get_user_model()


class TestContent(TestCase):
    HOME_URL = reverse('recipe_catalog:home')

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testUser', password='password123')
        cls.client_logged_in = Client()
        cls.client_logged_in.force_login(cls.user)

        cls.recipe_main = Recipe.objects.create(
            name='Тестовый рецепт',
            description='Описание тестового рецепта',
            author=cls.user,
        )

        cls.recipes = [
            Recipe(name=f'Рецепт {i}', description=f'Описание рецепта {i}', author=cls.user)
            for i in range(settings.OBJS_ON_PAGE + 5)
        ]
        Recipe.objects.bulk_create(cls.recipes)

        cls.ingredients = [
            Ingredient(name=f'Ингредиент {i}', recipe=cls.recipe_main) for i in range(5)
        ]
        Ingredient.objects.bulk_create(cls.ingredients)

    def test_home_page1(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page2(self):
        url = reverse('recipe_catalog:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_detail_ok(self):
        url = reverse('recipe_catalog:detail', args=[self.recipe_main.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # def test_home_page_recipe_count(self):
    #     """На главной странице отображается правильное количество рецептов."""
    #     response = self.client_logged_in.get(self.HOME_URL)
    #     recipes = response.context['recipes']
    #     self.assertEqual(len(recipes), settings.OBJS_ON_PAGE)

    def test_home_page_recipes_sorted_abc(self):
        """Рецепты на главной странице отсортированы по алфавиту."""
        response = self.client_logged_in.get(self.HOME_URL)
        recipes = response.context['recipes']
        recipe_names = [recipe.name for recipe in recipes]
        self.assertEqual(recipe_names, sorted(recipe_names))

    def test_home_page_content_displayed(self):
        """На главной странице отображается название и фото рецепта."""
        response = self.client_logged_in.get(self.HOME_URL)
        self.assertContains(response, self.recipe_main.name)
        self.assertContains(response, self.recipe_main.image)

    def test_recipe_detail_content_displayed(self):
        """Проверка отображения данных на странице рецепта"""
        url = reverse('recipe_catalog:detail', args=[self.recipe_main.pk])
        response = self.client_logged_in.get(url)

        self.assertContains(response, self.recipe_main.name)
        self.assertContains(response, self.recipe_main.description)
        self.assertContains(response, self.recipe_main.cooking_time)

        ingredients = response.context['ingredients']
        self.assertTrue(len(ingredients) > 0)

        self.assertContains(response, f"{self.recipe_main.total_calories()} ккал")
        self.assertContains(response, f"{self.recipe_main.total_weight()} г")

        self.assertContains(response, self.recipe_main.image.url)

    def test_recipe_detail_ingredients_sorted(self):
        """Ингредиенты на странице рецепта отсортированы по алфавиту."""
        url = reverse('recipe_catalog:detail', args=[self.recipe_main.pk])
        response = self.client_logged_in.get(url)
        ingredients = response.context['ingredients']
        ingredient_names = [ingredient.name for ingredient in ingredients]
        self.assertEqual(ingredient_names, sorted(ingredient_names))

    def test_404_for_nonexistent_recipe(self):
        """Запрос к несуществующему рецепту возвращает 404."""
        nonexistent_recipe_id = Recipe.objects.last().pk + 1
        url = reverse('recipe_catalog:detail', args=[nonexistent_recipe_id])
        response = self.client_logged_in.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
