# from django.test import TestCase
#
# # Create your tests here.
#
# from django.test import TestCase
#
# from ..models import Ingredient, Recipe, RecipeIngredient
#
#
# class TestOne(TestCase):
#     def test_always_true(self):
#         self.assertTrue(True)
#
#
# class TestOneDb(TestCase):
#     RECIPE_NAME = 'Яичница'
#     INGREDIENT_NAME = 'Яйцо'
#     @classmethod
#     def setUpTestData(cls):
#         cls.ingredient_egg = Ingredient.objects.create(
#             name=cls.INGREDIENT_NAME,
#         )
#         cls.recipe = Recipe.objects.create(
#             name=cls.RECIPE_NAME,
#         )
#         cls.recipe.ingredients.set([cls.ingredient_egg])
#
#     def test_successful_creation_ingredient(self):
#         ingredients_count = Ingredient.objects.count()
#         self.assertEqual(ingredients_count, 1)
#
#     def test_successful_creation_recipe(self):
#         recipe_count = Recipe.objects.count()
#         self.assertEqual(recipe_count, 1)
#
#     def test_successful_create_recipe_ingredient(self):
#         counts = [
#             (self.recipe.ingredients.count(), 1, "Рецепт"),
#             (RecipeIngredient.objects.count(), 1, "Ингредиент-Рецепт"),
#         ]
#         for cnt in counts:
#             with self.subTest(msg='Рецепты-ингредиенты'):
#                 self.assertEqual(cnt[0], cnt[1], cnt[2])
#
#     def test_titles(self):
#         titles = [
#             (self.ingredient_egg.name, self.INGREDIENT_NAME, 'Ингредиент'),
#             (self.recipe.name, self.RECIPE_NAME, 'Рецепт'),
#         ]
#         for name in titles:
#             with self.subTest(msg=f'Название {name[2]}'):
#                 self.assertEqual(name[0], name[1])
