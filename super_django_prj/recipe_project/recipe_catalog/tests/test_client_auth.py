from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Recipe, Ingredient

User = get_user_model()


class TestClientAuth(TestCase):
    HOME_URL = reverse('recipe_catalog:home')
    ABOUT_URL = reverse('recipe_catalog:about')
    DETAIL_URL = 'recipe_catalog:detail'

    ADMIN_RECIPE_CHANGE = 'admin:recipe_catalog_recipe_change'
    ADMIN_SLUG = '/admin/'

    RECIPE_1_NAME = 'Рецепт 1'
    RECIPE_1_DESC = 'Описание'
    INGREDIENT_1_NAME = 'Ингредиент 1'

    RECIPE_2_NAME = 'Рецепт 2'
    RECIPE_2_DESC = 'Описание'
    INGREDIENT_2_NAME = 'Ингредиент 2'

    @classmethod
    def setUpTestData(cls):
        cls.test_user_1 = User.objects.create_user(username='TestUser1', is_staff=True)
        cls.test_user_2 = User.objects.create_user(username='TestUser2', is_staff=True)

        cls.recipe_user_1 = Recipe.objects.create(
            name=cls.RECIPE_1_NAME,
            description=cls.RECIPE_1_DESC,
            author=cls.test_user_1
        )

        cls.recipe_user_2 = Recipe.objects.create(
            name=cls.RECIPE_2_NAME,
            description=cls.RECIPE_2_DESC,
            author=cls.test_user_2
        )

        cls.client_1 = Client()
        cls.client_1.force_login(cls.test_user_1)

        cls.client_2 = Client()
        cls.client_2.force_login(cls.test_user_2)

    def test_home_page_auth_access(self):
        """Главная страница доступна залогиненным пользователям."""
        for client in (self.client_1, self.client_2):
            with self.subTest(client=client):
                response = client.get(self.HOME_URL)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_page_auth_access(self):
        """Страница описания доступна залогиненному пользователю."""
        for client in (self.client_1, self.client_2):
            with self.subTest(client=client):
                response = client.get(self.ABOUT_URL)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_recipe_detail_auth_access(self):
        """Страница рецепта доступна залогиненному пользователям"""
        for recipe, client in (
                (self.recipe_user_1, self.client_1),
                (self.recipe_user_2, self.client_2),
        ):
            with self.subTest(recipe=recipe, client=client):
                url = reverse(self.DETAIL_URL, args=[recipe.pk])
                response = client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_login_page_auth_success(self):
        """Страница админки доступна залогиненным пользователям."""
        for client in (self.client_1, self.client_2):
            with self.subTest(client=client):
                response = client.get(self.ADMIN_SLUG)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_recipe_page_auth_success(self):
        """Редактирование своего рецепта доступно его автору."""
        for recipe, client in (
                (self.recipe_user_1, self.client_1),
                (self.recipe_user_2, self.client_2),
        ):
            with self.subTest(recipe=recipe, client=client):
                url = reverse(self.ADMIN_RECIPE_CHANGE, args=[recipe.pk])
                response = client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_author_recipe_page_auth(self):
        """Редактирование рецепта недоступно другому автору."""
        for recipe, client in (
                (self.recipe_user_1, self.client_2),
                (self.recipe_user_2, self.client_1),
        ):
            with self.subTest(recipe=recipe, client=client):
                url = reverse(self.ADMIN_RECIPE_CHANGE, args=[recipe.pk])
                response = client.get(url)
                self.assertEqual(response.status_code, 302)
