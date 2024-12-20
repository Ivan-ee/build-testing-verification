from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Recipe, Ingredient, MeasurementScale, RecipeIngredient

User = get_user_model()


class TestClientAuth(TestCase):
    RECIPE_1_NAME = 'Рецепт 1'
    RECIPE_1_DESC = 'Описание'
    RECIPE_1_COOKING_TIME = 10
    INGREDIENT_1_NAME = 'Ингредиент 1'
    INGREDIENT_1_CALORIES = 100
    INGREDIENT_2_NAME = 'Ингредиент 2'
    INGREDIENT_2_CALORIES = 200
    NEW_RECIPE_NAME = "Новый рецепт"
    NEW_RECIPE_DESCRIPTION = "Новое описание"
    NEW_INGREDIENT_NAME = "Новый ингредиент"
    NEW_INGREDIENT_CALORIES = 300

    @classmethod
    def setUpTestData(cls):
        cls.test_user_1 = User.objects.create_user(username='TestUser1', is_staff=True)
        cls.test_user_2 = User.objects.create_user(username='TestUser2', is_staff=True)
        cls.scale = MeasurementScale.objects.create(label="г", key="gg", abbreviation="г")
        cls.ingredient_1 = Ingredient.objects.create(
            name=cls.INGREDIENT_1_NAME,
            calories=cls.INGREDIENT_1_CALORIES
        )
        cls.ingredient_2 = Ingredient.objects.create(
            name=cls.INGREDIENT_2_NAME,
            calories=cls.INGREDIENT_2_CALORIES
        )

        cls.client_1 = Client()
        cls.client_1.force_login(cls.test_user_1)

        cls.client_2 = Client()
        cls.client_2.force_login(cls.test_user_2)

        cls.form_data_recipe = {
            "name": cls.NEW_RECIPE_NAME,
            "description": cls.NEW_RECIPE_DESCRIPTION,
            "cooking_time": cls.RECIPE_1_COOKING_TIME,
            "recipeingredient_set-TOTAL_FORMS": "1",
            "recipeingredient_set-INITIAL_FORMS": "0",
            "recipeingredient_set-MIN_NUM_FORMS": "0",
            "recipeingredient_set-MAX_NUM_FORMS": "1000",
            "recipeingredient_set-0-ingredient": cls.ingredient_1.pk,
            "recipeingredient_set-0-unit": cls.scale.pk,
            "recipeingredient_set-0-weight_by_pcs": "",
            "recipeingredient_set-0-count": 100,
        }
        cls.form_data_ingredient = {
            "name": cls.NEW_INGREDIENT_NAME,
            "calories": cls.NEW_INGREDIENT_CALORIES
        }

    def test_author_can_create_recipe(self):
        """Авторизованный пользователь может создать рецепт."""
        recipes_before = Recipe.objects.count()
        response = self.client_1.post(reverse('recipe_catalog:recipe_create'), data=self.form_data_recipe)
        self.assertEqual(response.status_code, 302, "Должен быть редирект после создания рецепта")
        recipes_after = Recipe.objects.count()
        self.assertEqual(recipes_before + 1, recipes_after, "Рецепт должен быть создан")
        new_recipe = Recipe.objects.latest('pk')
        with self.subTest(msg="Проверка создания рецепта"):
            self.assertEqual(new_recipe.author, self.test_user_1, "Авторство установлено верно")
            self.assertEqual(new_recipe.name, self.NEW_RECIPE_NAME, "Имя установлено верно")
            self.assertEqual(new_recipe.description, self.NEW_RECIPE_DESCRIPTION, "Описание установлено верно")

    def test_author_can_create_ingredient(self):
        """Авторизованный пользователь может создать ингредиент."""
        ingredients_before = Ingredient.objects.count()
        response = self.client_1.post(reverse('recipe_catalog:ingredient'), data=self.form_data_ingredient)
        self.assertEqual(response.status_code, HTTPStatus.OK, "Должен быть HTTPStatus.OK после создания ингредиента")
        ingredients_after = Ingredient.objects.count()
        self.assertEqual(ingredients_before + 1, ingredients_after, "Ингредиент должен быть создан")
        new_ingredient = Ingredient.objects.latest('pk')
        with self.subTest(msg="Проверка создания ингредиента"):
            self.assertEqual(new_ingredient.name, self.NEW_INGREDIENT_NAME, "Имя установлено верно")
            self.assertEqual(new_ingredient.calories, self.NEW_INGREDIENT_CALORIES, "Калории установлены верно")

    def test_author_can_delete_recipe(self):
        """Автор может удалить свой рецепт"""
        recipe_user_1 = Recipe.objects.create(
            name=self.RECIPE_1_NAME,
            description=self.RECIPE_1_DESC,
            author=self.test_user_1,
            cooking_time=self.RECIPE_1_COOKING_TIME,
        )
        with self.subTest(msg="Автор может удалить свой рецепт"):
            url_delete = reverse('recipe_catalog:recipe_delete', args=[recipe_user_1.pk])
            count_before = Recipe.objects.count()
            response_delete = self.client_1.post(url_delete)
            self.assertEqual(response_delete.status_code, HTTPStatus.FOUND, "Автор может удалить свой рецепт")
            count_after = Recipe.objects.count()
            self.assertEqual(count_before - 1, count_after, "Рецепт должен быть удален")

    def test_author_can_edit_recipe(self):
        """Автор может редактировать свой рецепт"""
        recipe_user_1 = Recipe.objects.create(
            name=self.RECIPE_1_NAME,
            description=self.RECIPE_1_DESC,
            author=self.test_user_1,
            cooking_time=self.RECIPE_1_COOKING_TIME,
        )
        url_edit = reverse('recipe_catalog:recipe_edit', args=[recipe_user_1.pk])
        response_edit = self.client_1.post(url_edit, data={"name": "New Name"})
        self.assertEqual(response_edit.status_code, 200, "Автор может отредактировать свой рецепт")
        recipe_user_1.refresh_from_db()
        with self.subTest(msg="Проверка редактирования рецепта"):
            self.assertEqual(recipe_user_1.name, "New Name", "Имя рецепта должно обновиться")

    def test_author_can_edit_ingredient(self):
        """Автор может редактировать свой ингредиент"""
        url_edit = reverse('recipe_catalog:ingredient_edit', args=[self.ingredient_1.pk])
        response_edit = self.client_1.post(url_edit, data={"name": "New Name", "calories": 200})
        self.assertEqual(response_edit.status_code, HTTPStatus.OK, "Автор может редактировать свой ингредиент")
        self.ingredient_1.refresh_from_db()
        with self.subTest(msg="Проверка редактирования ингредиента"):
            self.assertEqual(self.ingredient_1.name, "New Name", "Имя ингредиента должно обновиться")

    def test_author_can_delete_ingredient(self):
        """Автор может удалить свой ингредиент"""
        url_delete = reverse('recipe_catalog:ingredient_delete', args=[self.ingredient_1.pk])
        count_before = Ingredient.objects.count()
        response_delete = self.client_1.post(url_delete)
        self.assertEqual(response_delete.status_code, HTTPStatus.FOUND, "Автор может удалить свой ингредиент")
        count_after = Ingredient.objects.count()
        self.assertEqual(count_before - 1, count_after, "Ингредиент должен быть удален")

    def test_auth_user_can_access_my_recipes(self):
        """Авторизованный пользователь может получить доступ к странице мои рецепты"""
        response = self.client_1.get(reverse('recipe_catalog:my_recipes'))
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         "Авторизованный пользователь может получить доступ к странице мои рецепты")

    def test_auth_user_can_access_ingredients_list(self):
        """Авторизованный пользователь может получить доступ к странице ингредиенты"""
        response = self.client_1.get(reverse('recipe_catalog:ingredients_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         "Авторизованный пользователь может получить доступ к странице ингредиенты")
