from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import render, get_object_or_404

from .models import Recipe


def about(request):
    template_name = 'recipe_catalog/about.html'

    return render(request, template_name)


def index(request):
    template_name = 'recipe_catalog/index.html'
    recipes_list = Recipe.objects.order_by('name')
    paginator = Paginator(recipes_list, settings.OBJS_ON_PAGE)

    page_number = request.GET.get('page')
    recipes = paginator.get_page(page_number)

    context = {
        'recipes': recipes
    }

    return render(request, template_name, context)


def detail(request, pk):
    template_name = 'recipe_catalog/recipe.html'
    recipe = get_object_or_404(Recipe, pk=pk)

    ingredients = []
    for ri in recipe.recipeingredient_set.select_related('ingredient', 'unit').order_by('ingredient__name'):
        ingredient = ri.ingredient
        if ri.unit:
            unit_label = ri.unit.abbreviation or ri.unit.label
            unit = f"{ri.count} {unit_label}"
        else:
            unit = f"{ri.count} г"

        ingredients.append({
            'name': ingredient.name,
            'unit': unit,
        })

    context = {
        'title': recipe.name,
        'description': recipe.description,
        'cooking_time': recipe.cooking_time,
        'total_weight': recipe.total_weight(),
        'total_calories': recipe.total_calories(),
        'ingredients': ingredients,
        'image': recipe.image.url,
    }

    return render(request, template_name, context)
