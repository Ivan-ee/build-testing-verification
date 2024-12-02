from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Recipe, Ingredient

User = get_user_model()


class TestClientAnonymous(TestCase):
    HOME_URL = reverse('recipe_catalog:home')
    DETAIL_URL = 'recipe_catalog:detail'

    RECIPE_NAME = 'Яичница'
    RECIPE_DESC = 'Вкусная яичница'
    INGREDIENT_NAME = 'Яйцо'

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        cls.recipe = Recipe.objects.create(
            name=cls.RECIPE_NAME,
            description=cls.RECIPE_DESC,
        )

    def test_home_page_anonymous_access(self):
        """Главная страница доступна анонимному пользователю."""
        response = self.client.get(self.HOME_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_recipe_detail_anonymous_access(self):
        """Страница рецепта доступна анонимному пользователю."""
        url = reverse(self.DETAIL_URL, args=[self.recipe.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_anonymous_to_login(self):
        """Анонимный пользователь перенаправляется на страницу логина при попытке войти в ЛК."""
        response = self.client.get('/admin/')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/admin/login/?next=/admin/")

    def test_login_page_anonymous_success(self):
        """Страница логина доступна анонимному пользователю"""
        response = self.client.get('/admin/login/?next=/admin/')

        self.assertEqual(response.status_code, HTTPStatus.OK)
