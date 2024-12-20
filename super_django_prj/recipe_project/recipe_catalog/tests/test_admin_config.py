from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from ..admin import RecipeAdmin, IngredientAdmin, IngredientInline
from ..models import Recipe, Ingredient

User = get_user_model()


class TestAdminConfig(TestCase):
    """Тесты для конфигурации Django Admin."""

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username="test_admin", is_staff=True)
        cls.test_user_2 = User.objects.create_user(username="test_admin2")
        cls.test_recipe = Recipe.objects.create(name="Тестовый рецепт", author=cls.test_user, cooking_time=10)
        cls.test_ingredient = Ingredient.objects.create(name="Тестовый ингредиент", calories=100)

        cls.factory = RequestFactory()
        cls.admin_site = AdminSite()

    def test_recipe_admin_list_display(self):
        """Проверка list_display для RecipeAdmin"""
        recipe_admin = RecipeAdmin(Recipe, self.admin_site)
        expected_list = ["name", "author", "cooking_time", "total_weight_display", "total_calories_display"]
        self.assertEqual(recipe_admin.list_display, expected_list, "Проверьте список полей list_display")

    def test_recipe_admin_readonly_fields(self):
        """Проверка readonly_fields для RecipeAdmin"""
        recipe_admin = RecipeAdmin(Recipe, self.admin_site)
        expected_fields = ["author", "image_tag", "total_weight_display", "total_calories_display"]
        self.assertEqual(recipe_admin.readonly_fields, expected_fields, "Проверьте список полей readonly_fields")

    def test_recipe_admin_inlines(self):
        """Проверка inlines для RecipeAdmin"""
        recipe_admin = RecipeAdmin(Recipe, self.admin_site)
        self.assertEqual(recipe_admin.inlines, [IngredientInline], "Проверьте inlines")

    def test_recipe_admin_total_weight_display(self):
        """Проверка total_weight_display RecipeAdmin"""
        recipe_admin = RecipeAdmin(Recipe, self.admin_site)
        self.test_recipe.total_weight = lambda: 123
        self.assertEqual(recipe_admin.total_weight_display(self.test_recipe), "123", "Проверьте total_weight_display")

    def test_recipe_admin_total_calories_display(self):
        """Проверка total_calories_display RecipeAdmin"""
        recipe_admin = RecipeAdmin(Recipe, self.admin_site)
        self.test_recipe.total_calories = lambda: 456
        self.assertEqual(recipe_admin.total_calories_display(self.test_recipe), "456",
                         "Проверьте total_calories_display")

    def test_recipe_admin_get_queryset_superuser(self):
        """Проверка get_queryset для суперпользователя"""
        request = self.factory.get('/')
        request.user = self.test_user
        request.user.is_superuser = True
        recipe_admin = RecipeAdmin(Recipe, self.admin_site)
        queryset = recipe_admin.get_queryset(request)
        self.assertEqual(queryset.count(), 1, "Суперпользователь должен видеть все рецепты.")

    def test_recipe_admin_get_queryset_not_superuser(self):
        """Проверка get_queryset для обычного пользователя"""
        request = self.factory.get('/')
        request.user = self.test_user_2
        recipe_admin = RecipeAdmin(Recipe, self.admin_site)
        queryset = recipe_admin.get_queryset(request)
        self.assertEqual(queryset.count(), 0, "Обычный пользователь должен видеть только свои рецепты")

    def test_recipe_admin_has_change_permission_superuser(self):
        """Проверка has_change_permission для суперпользователя"""
        request = self.factory.get('/')
        request.user = self.test_user
        request.user.is_superuser = True
        recipe_admin = RecipeAdmin(Recipe, self.admin_site)
        self.assertTrue(recipe_admin.has_change_permission(request, self.test_recipe),
                        "Суперпользователь должен менять")

    def test_recipe_admin_has_change_permission_author(self):
        """Проверка has_change_permission для автора"""
        request = self.factory.get('/')
        request.user = self.test_user
        recipe_admin = RecipeAdmin(Recipe, self.admin_site)
        self.assertTrue(recipe_admin.has_change_permission(request, self.test_recipe), "Автор может менять свой рецепт")

    def test_recipe_admin_has_change_permission_not_author(self):
        """Проверка has_change_permission для не автора"""
        request = self.factory.get('/')
        request.user = self.test_user_2
        recipe_admin = RecipeAdmin(Recipe, self.admin_site)
        self.assertFalse(recipe_admin.has_change_permission(request, self.test_recipe),
                         "Не автор не может менять чужой рецепт")

    def test_recipe_admin_has_delete_permission_superuser(self):
        """Проверка has_delete_permission для суперпользователя"""
        request = self.factory.get('/')
        request.user = self.test_user
        request.user.is_superuser = True
        recipe_admin = RecipeAdmin(Recipe, self.admin_site)
        self.assertTrue(recipe_admin.has_delete_permission(request, self.test_recipe),
                        "Суперпользователь может удалить")

    def test_recipe_admin_has_delete_permission_author(self):
        """Проверка has_delete_permission для автора"""
        request = self.factory.get('/')
        request.user = self.test_user
        recipe_admin = RecipeAdmin(Recipe, self.admin_site)
        self.assertTrue(recipe_admin.has_delete_permission(request, self.test_recipe),
                        "Автор может удалить свой рецепт")

    def test_recipe_admin_has_delete_permission_not_author(self):
        """Проверка has_delete_permission для не автора"""
        request = self.factory.get('/')
        request.user = self.test_user_2
        recipe_admin = RecipeAdmin(Recipe, self.admin_site)
        self.assertFalse(recipe_admin.has_delete_permission(request, self.test_recipe),
                         "Не автор не может удалить чужой рецепт")

    def test_recipe_admin_save_model(self):
        """Проверка save_model для установки автора"""
        request = self.factory.get('/')
        request.user = self.test_user_2
        recipe_admin = RecipeAdmin(Recipe, self.admin_site)
        new_recipe = Recipe(name="Новый рецепт")
        recipe_admin.save_model(request, new_recipe, None, None)
        self.assertEqual(new_recipe.author, self.test_user_2, "Автор должен установится в методе save_model")

    def test_ingredient_admin_list_display(self):
        """Проверка list_display для IngredientAdmin"""
        ingredient_admin = IngredientAdmin(Ingredient, self.admin_site)
        expected_list = ["name"]
        self.assertEqual(ingredient_admin.list_display, expected_list, "Проверьте список полей list_display")

    def test_ingredient_inline_fields(self):
        """Проверка отображения полей в IngredientInline"""
        self.assertEqual(IngredientInline.fields, ['ingredient', 'unit', "weight_by_pcs", 'count'], "Проверьте поля")
