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

    context = {
        'title': recipe.name,
        'description': recipe.description,
        'cooking_time': recipe.cooking_time,
        'total_weight': recipe.total_weight(),
        'total_calories': recipe.total_calories(),
        'ingredients': recipe.recipeingredient_set.select_related('ingredient').order_by('ingredient__name')
    }

    return render(request, template_name, context)
