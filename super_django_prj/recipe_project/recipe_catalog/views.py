from django.http import HttpResponse
from django.shortcuts import render

from .models import Recipe


def about(request):
    template_name = 'recipe_catalog/about.html'

    return render(request, template_name)


def index(request):
    template_name = 'recipe_catalog/index.html'

    return render(request, template_name)


def recipe_detail(request, pk):
    template_name = 'recipe_catalog/recipe.html'

    # title = 'Блинчики с мясом'
    # context = {'title': title, 'recipe_id': pk}
    #
    # return render(request, template_name, context)

    recipe = Recipe.objects.get(pk=pk)
    context = {
        'title': recipe.name,
        'recipe_id': pk,
        'ingredients': recipe.ingredients.order_by('name')
    }

    return render(request, template_name, context)

