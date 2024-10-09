from typing import Union

from pr_2.error.error import *


class Ingredient:
    def __init__(
            self,
            name: str,
            raw_weight: Union[int, float],
            weight: Union[int, float],
            cost: Union[int, float],
    ) -> None:
        self.name = name
        self.raw_weight = raw_weight
        self.weight = weight
        self.cost = cost

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ErrNotString
        if not value.strip():
            raise ErrNotEmpty
        self._name = value

    @property
    def raw_weight(self):
        return self._raw_weight

    @raw_weight.setter
    def raw_weight(self, value):
        if not isinstance(value, (int, float)):
            raise ErrNotNumber
        if value <= 0:
            raise ErrNotPositive
        self._raw_weight = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if not isinstance(value, (int, float)):
            raise ErrNotNumber
        if value <= 0:
            raise ErrNotPositive
        self._weight = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        if not isinstance(value, (int, float)):
            raise ErrNotNumber
        if value < 0:
            raise ErrNotPositive
        self._cost = value


class Receipt:
    def __init__(self, name: str, ingredient_list: list[tuple[str, float, float, float]]) -> None:
        self.name = name
        self.ingredients = [
            Ingredient(name, raw_weight, weight, cost)
            for name, raw_weight, weight, cost in ingredient_list
        ]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ErrNotString
        if not value.strip():
            raise ErrNotEmpty
        self._name = value

    @property
    def ingredients(self):
        return self._ingredients

    @ingredients.setter
    def ingredients(self, value: list[Ingredient]):
        if not isinstance(value, list):
            raise ErrNotList
        if not all(isinstance(ingredient, Ingredient) for ingredient in value):
            raise ErrNotIngredient
        if not value:
            raise ErrNotEmpty
        self._ingredients = value

    def calc_cost(self, portions=1):
        total_cost = sum(ingredient.cost for ingredient in self.ingredients)
        return total_cost * portions

    def calc_weight(self, portions=1, raw=True):
        if raw:
            total_weight = sum(ingredient.raw_weight for ingredient in self.ingredients)
        else:
            total_weight = sum(ingredient.weight for ingredient in self.ingredients)
        return total_weight * portions


#

