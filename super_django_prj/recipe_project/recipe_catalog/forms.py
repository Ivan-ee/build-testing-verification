from django import forms
from django.forms import inlineformset_factory

from .models import Ingredient, Recipe, RecipeIngredient


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name', 'calories')
        labels = {
            'name': 'Название',
            'calories': 'Калории',
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'description', 'image', 'cooking_time')
        labels = {
            'name': 'Название блюда',
            'description': 'Описание',
            'image': 'Изображение',
            'cooking_time': 'Время приготовления (мин)',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'unit', 'weight_by_pcs', 'count')
        labels = {
            'ingredient': 'Ингредиент',
            'unit': 'Единица измерения',
            'weight_by_pcs': 'Вес шт/гр (опционально)',
            'count': 'Количество',
        }


RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=2,
    can_delete=True,
)
