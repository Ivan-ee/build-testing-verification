from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Recipe


class TestClientAnonymous(TestCase):
    HOME_URL = reverse('recipe_catalog:home')
    ABOUT_URL = reverse('recipe_catalog:about')
    DETAIL_URL = 'recipe_catalog:detail'

    RECIPE_NAME = 'Яичница'
    RECIPE_DESC = 'Вкусная яичница'
    INGREDIENT_NAME = 'Яйцо'

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.test_user_1 = User.objects.create_user(username='TestUser1', password='111')
        cls.recipe = Recipe.objects.create(
            name=cls.RECIPE_NAME,
            description=cls.RECIPE_DESC,
            author=cls.test_user_1,
        )

    def test_pages_anonymous_access(self):
        """Главная и страница описания доступны анонимному пользователю."""
        urls = [
            (self.HOME_URL, HTTPStatus.OK),
            (self.ABOUT_URL, HTTPStatus.OK),
        ]
        for url, expected_status in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_recipe_detail_anonymous_access(self):
        """Страница рецепта доступна анонимному пользователю."""
        url = reverse(self.DETAIL_URL, args=[self.recipe.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_anonymous_to_login(self):
        """Вход в админку"""
        response = self.client.get('/admin/')

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, "/admin/login/?next=/admin/")

    def test_login_page_anonymous_success(self):
        """Страница логина доступна анонимному пользователю."""
        url = '/admin/login/?next=/admin/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
