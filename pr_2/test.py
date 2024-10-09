import unittest

from main import Ingredient, Receipt


class TestIngredient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid_ingredient_data = {
            "name": "Свекла",
            "raw_weight": 250,
            "weight": 180,
            "cost": 50
        }

    def setUp(self):
        self.ingredient = Ingredient(
            self.valid_ingredient_data['name'],
            self.valid_ingredient_data['raw_weight'],
            self.valid_ingredient_data['weight'],
            self.valid_ingredient_data['cost']
        )

    def tearDown(self):
        del self.ingredient

    @classmethod
    def tearDownClass(cls):
        cls.valid_ingredient_data = None

    def test_valid_ingredient(self):
        self.assertEqual(self.ingredient.name, "Свекла")
        self.assertEqual(self.ingredient.raw_weight, 250)
        self.assertEqual(self.ingredient.weight, 180)
        self.assertEqual(self.ingredient.cost, 50)

    def test_invalid_raw_weight(self):
        with self.assertRaises(ValueError):
            Ingredient("Свекла", -250, 180, 50)
        with self.assertRaises(ValueError):
            Ingredient("Свекла", 0, 180, 50)
        with self.assertRaises(ValueError):
            Ingredient("Свекла", "есть", 180, 50)

    def test_invalid_weight(self):
        with self.assertRaises(ValueError):
            Ingredient("Свекла", 80, -10, 20)
        with self.assertRaises(ValueError):
            Ingredient("Свекла", 80, 0, 20)
        with self.assertRaises(ValueError):
            Ingredient("Свекла", 80, "есть", 20)

    def test_invalid_cost(self):
        with self.assertRaises(ValueError):
            Ingredient("Свекла", 80, 70, -10)
        with self.assertRaises(ValueError):
            Ingredient("Свекла", 80, 70, 0)
        with self.assertRaises(ValueError):
            Ingredient("Свекла", 80, 70, "есть")

    def test_boundary_cost(self):
        cost = 1000
        ingredient = Ingredient("Свекла", 80, 70, cost)
        self.assertEqual(ingredient.cost, cost)

    def test_float_weights_and_cost(self):
        ingredient = Ingredient("Яйцо", 80.5, 70.5, 19.99)
        self.assertEqual(ingredient.raw_weight, 80.5)
        self.assertEqual(ingredient.weight, 70.5)
        self.assertEqual(ingredient.cost, 19.99)

    def test_name_as_non_string(self):
        with self.assertRaises(ValueError):
            Ingredient(123, 80, 70, 20)

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            Ingredient("", 80, 70, 20)


class TestReceiptSurname(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt_from_api_beet = {
            "title": "Свекольник",
            "ingredients_list": [
                ("Свекла", 250, 180, 50),
                ("Картофель", 200, 200, 30),
                ("Морковь", 150, 150, 40),
                ("Лук", 50, 50, 60),
                ("Яйца", 100, 70, 120),
                ("Укроп", 15, 15, 40),
                ("Сметана", 60, 60, 80),
            ]
        }

    def setUp(self):
        self.receipt_beet = Receipt(
            self.receipt_from_api_beet["title"],
            self.receipt_from_api_beet["ingredients_list"]
        )

    def tearDown(self):
        del self.receipt_beet

    @classmethod
    def tearDownClass(cls):
        cls.receipt_from_api_beet = None

    def test_valid_receipt(self):
        self.assertEqual(self.receipt_beet.name, "Свекольник")
        self.assertEqual(len(self.receipt_beet.ingredients), 7)

    def test_calc_cost(self):
        self.assertEqual(self.receipt_beet.calc_cost(), 420)
        self.assertEqual(self.receipt_beet.calc_cost(2), 840)

    def test_calc_weight(self):
        self.assertEqual(self.receipt_beet.calc_weight(), 825)
        self.assertEqual(self.receipt_beet.calc_weight(raw=False), 725)
        self.assertEqual(self.receipt_beet.calc_weight(portions=2), 1650)

    def test_invalid_ingredient_list_empty(self):
        with self.assertRaises(ValueError):
            Receipt("Свекольник", [])

    def test_invalid_ingredient_list(self):
        with self.assertRaises(ValueError):
            Receipt("Свекольник", [("Сахар", -100, 90, 50)])

    def test_receipt_with_single_ingredient(self):
        receipt_single = Receipt("Блюдо", [("Вода", 100, 100, 10)])
        self.assertEqual(receipt_single.calc_cost(), 10)
        self.assertEqual(receipt_single.calc_weight(), 100)


if __name__ == "__main__":
    unittest.main()
