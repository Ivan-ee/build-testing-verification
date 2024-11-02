from django.http import HttpResponse
from django.shortcuts import render


def about(request):
    return HttpResponse("О проекте")


def index(request):
    template_name = 'recipe_catalog/index.html'

    return render(request, template_name)


def recipe_detail(request, pk):
    template_name = 'recipe_catalog/recipe.html'

    title = 'Блинчики с мясом'
    context = {'title': title, 'recipe_id': pk}

    return render(request, template_name, context)
