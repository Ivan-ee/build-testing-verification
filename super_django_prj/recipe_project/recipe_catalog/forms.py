from django import forms

from .models import Ingredient


class IngredientForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'calories')
        labels = {
            'name': 'Название',
            'calories': 'Калории',
        }
        model = Ingredient
