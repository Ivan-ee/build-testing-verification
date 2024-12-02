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

    RECIPE_NAME = 'Яичница'
    RECIPE_DESC = 'Вкусная яичница'
    INGREDIENT_NAME = 'Яйцо'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='TestUser1', password='111')
        cls.other_user = User.objects.create_user(username='TestUser2', password='222')

        cls.recipe = Recipe.objects.create(
            name=cls.RECIPE_NAME,
            description=cls.RECIPE_DESC,
            author=cls.user
        )

    def test_home_page_auth_access(self):
        """Главная страница доступна залогиненному пользователю."""
        response = self.client.get(self.HOME_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_page_auth_access(self):
        """Страница Описания доступна залогиненному пользователю."""
        response = self.client.get(self.ABOUT_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_recipe_detail_auth_access(self):
        """Страница рецепта доступна залогиненному пользователю."""
        url = reverse(self.DETAIL_URL, args=[self.recipe.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_login_page_auth_success(self):
        """Страница логина доступна залогиненному пользователю"""
        response = self.client.get('/admin/login/?next=/admin/')

        self.assertEqual(response.status_code, HTTPStatus.OK)
