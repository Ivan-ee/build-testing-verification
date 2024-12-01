from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Recipe


def about(request):
    template_name = 'recipe_catalog/about.html'

    return render(request, template_name)


def index(request):
    template_name = 'recipe_catalog/index.html'
    recipes = Recipe.objects.all()

    context = {
        'recipes': recipes
    }

    return render(request, template_name, context)


def recipe_detail(request, pk):
    template_name = 'recipe_catalog/recipe.html'
    recipe = get_object_or_404(Recipe, pk=pk)

    ingredients = []
    for ri in recipe.recipeingredient_set.select_related('ingredient').order_by('ingredient__name'):
        ingredient = ri.ingredient
        if ingredient.unit and ingredient.unit.key == 'pcs':
            weight = ri.count * ingredient.weight_by_pcs
            unit = f"{ri.count} шт"
        else:
            unit = f"{ri.count} {ingredient.unit.label}" if ingredient.unit else f"{ri.count} г"
        ingredients.append({
            'name': ingredient.name,
            'unit': unit
        })

    context = {
        'title': recipe.name,
        'description': recipe.description,
        'cooking_time': recipe.cooking_time,
        'total_weight': recipe.total_weight(),
        'total_calories': recipe.total_calories(),
        'ingredients': ingredients,
    }

    return render(request, template_name, context)
