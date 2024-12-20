from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Recipe, Ingredient


class TestClientAnonymous(TestCase):
    HOME_URL = reverse('recipe_catalog:home')
    ABOUT_URL = reverse('recipe_catalog:about')
    DETAIL_URL = 'recipe_catalog:detail'
    RECIPE_CREATE_URL = reverse('recipe_catalog:recipe_create')
    INGREDIENT_CREATE_URL = reverse('recipe_catalog:ingredient')
    INGREDIENTS_LIST_URL = reverse('recipe_catalog:ingredients_list')
    MY_RECIPES_URL = reverse('recipe_catalog:my_recipes')
    RECIPE_EDIT_URL = 'recipe_catalog:recipe_edit'
    RECIPE_DELETE_URL = 'recipe_catalog:recipe_delete'
    INGREDIENT_EDIT_URL = 'recipe_catalog:ingredient_edit'
    INGREDIENT_DELETE_URL = 'recipe_catalog:ingredient_delete'

    RECIPE_NAME = 'Яичница'
    RECIPE_DESC = 'Вкусная яичница'
    INGREDIENT_NAME = 'Яйцо'
    RECEIPT_STEPS = 'Процесс приготовления...'

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.test_user_1 = User.objects.create_user(username='TestUser1', password='111')
        cls.recipe = Recipe.objects.create(
            name=cls.RECIPE_NAME,
            description=cls.RECIPE_DESC,
            author=cls.test_user_1,
        )

        cls.url_recipe_create = reverse('recipe_catalog:recipe_create')
        cls.url_ingredient_create = reverse('recipe_catalog:ingredient')

        cls.data_recipe = {'title': 'Test Recipe'}
        cls.data_ingredient = {'title': 'Test Ingredient'}

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

    def test_anonymous_user_cant_create_recipe(self):
        """Анонимный пользователь не может создать рецепт"""
        response = self.client.get(self.RECIPE_CREATE_URL)
        self.assertRedirects(response, f'/auth/login/?next={self.RECIPE_CREATE_URL}')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        self.client.post(self.url_recipe_create, data=self.data_recipe)
        recipes_count = Recipe.objects.count()
        self.assertEqual(recipes_count, 1)

    def test_anonymous_user_cant_create_ingredient(self):
        """Анонимный пользователь не может создать ингредиент"""
        response = self.client.get(self.INGREDIENT_CREATE_URL)
        self.assertRedirects(response, f'/auth/login/?next={self.INGREDIENT_CREATE_URL}')
        self.assertEqual(response.status_code, 302)

        self.client.post(self.url_ingredient_create, data=self.data_ingredient)
        recipes_count = Ingredient.objects.count()
        self.assertEqual(recipes_count, 0)

    def test_anonymous_user_cant_access_ingredients_list(self):
        """Анонимный пользователь не может просмотреть список ингредиентов"""
        response = self.client.get(self.INGREDIENTS_LIST_URL)
        self.assertRedirects(response, f'/auth/login/?next={self.INGREDIENTS_LIST_URL}')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_anonymous_user_cant_access_my_recipes(self):
        """Анонимный пользователь не может просмотреть свои рецепты"""
        response = self.client.get(self.MY_RECIPES_URL)
        self.assertRedirects(response, f'/auth/login/?next={self.MY_RECIPES_URL}')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_anonymous_user_cant_edit_recipe(self):
        """Анонимный пользователь не может редактировать рецепт"""
        url = reverse(self.RECIPE_EDIT_URL, args=[self.recipe.pk])
        response = self.client.get(url)
        self.assertRedirects(response, f'/auth/login/?next={url}')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_anonymous_user_cant_delete_recipe(self):
        """Анонимный пользователь не может удалить рецепт"""
        url = reverse(self.RECIPE_DELETE_URL, args=[self.recipe.pk])
        response = self.client.get(url)
        self.assertRedirects(response, f'/auth/login/?next={url}')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_anonymous_user_cant_edit_ingredient(self):
        """Анонимный пользователь не может редактировать ингредиент"""
        url = reverse(self.INGREDIENT_EDIT_URL, args=[1])
        response = self.client.get(url)
        self.assertRedirects(response, f'/auth/login/?next={url}')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_anonymous_user_cant_delete_ingredient(self):
        """Анонимный пользователь не может удалить ингредиент"""
        url = reverse(self.INGREDIENT_DELETE_URL, args=[1])
        response = self.client.get(url)
        self.assertRedirects(response, f'/auth/login/?next={url}')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

