# from http import HTTPStatus
#
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.test import TestCase, Client
# from django.urls import reverse
#
# from ..models import Recipe
#
# User = get_user_model()
#
#
# class TestCatalog(TestCase):
#     RECIPE_NAME = 'Яичница'
#     HOME_URL = reverse('recipe_catalog:home')
#
#     @classmethod
#     def setUpTestData(cls):
#         all_recipes = []
#         cls.user = User.objects.create(username='testUser')
#         cls.client_logged_in = Client()
#         cls.client_logged_in.force_login(cls.user)
#
#         cls.recipe = Recipe.objects.create(
#             name=cls.RECIPE_NAME,
#         )
#
#         for index in range(settings.OBJS_ON_PAGE - 1):
#             news = Recipe(
#                 name=f'Рецепт {index}')
#             all_recipes.append(news)
#         Recipe.objects.bulk_create(all_recipes)
#
#     def test_home_page1(self):
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_home_page2(self):
#         url = reverse('recipe_catalog:home')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#
#     def test_detail_ok(self):
#         url = reverse('recipe_catalog:detail', args=[self.recipe.pk])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#
#     def test_home_count_recipes(self):
#         response = self.client.get(self.HOME_URL)
#         object_list = response.context['recipes']
#         news_count = object_list.count()
#         self.assertEqual(news_count, settings.OBJS_ON_PAGE)
