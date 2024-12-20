from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import IngredientForm, RecipeForm, RecipeIngredientForm, RecipeIngredientFormSet
from .models import Recipe, Ingredient, RecipeIngredient


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


def ingredients(request):
    template_name = 'recipe_catalog/ingredients.html'


@login_required
def ingredient(request):
    template = 'recipe_catalog/ingredient_form.html'
    form = IngredientForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        form.save()
    context = {'form': form}
    return render(request, template, context)


@login_required
def ingredient_edit(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    template = 'recipe_catalog/ingredient_form.html'
    instance = get_object_or_404(Ingredient, pk=pk)
    form = IngredientForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, template, context)


@login_required
def ingredient_delete(request, pk):
    template = 'recipe_catalog/ingredient_form.html'
    instance = get_object_or_404(Ingredient, pk=pk)
    form = IngredientForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('recipe_catalog:ingredients_list')
    return render(request, template, context)


@login_required
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        formset = RecipeIngredientFormSet(request.POST, instance=Recipe())

        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            formset.instance = recipe
            formset.save()
            return redirect(reverse('recipe_catalog:my_recipes'))
    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet(instance=Recipe())
    return render(request, 'recipe_catalog/recipe_form.html', {
        'form': form,
        'formset': formset
    })


@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.author != request.user:
        return redirect('recipe_catalog:home')

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        formset = RecipeIngredientFormSet(request.POST, instance=recipe)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect(reverse('recipe_catalog:my_recipes'))

    else:
        form = RecipeForm(instance=recipe)
        formset = RecipeIngredientFormSet(instance=recipe)

    return render(request, 'recipe_catalog/recipe_form.html', {
        'form': form,
        'formset': formset
    })


@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.author != request.user:
        return redirect('recipe_catalog:home')

    if request.method == "POST":
        recipe.delete()
        return redirect(reverse('recipe_catalog:my_recipes'))
    return render(request, 'recipe_catalog/recipe_confirm_delete.html', {'recipe': recipe})


@login_required
def my_recipes(request):
    template_name = 'recipe_catalog/index.html'
    recipes_list = Recipe.objects.filter(author=request.user).order_by('name')
    paginator = Paginator(recipes_list, settings.OBJS_ON_PAGE)

    page_number = request.GET.get('page')
    recipes = paginator.get_page(page_number)

    context = {
        'recipes': recipes
    }

    return render(request, template_name, context)


@login_required
def ingredients_list(request):
    template_name = 'recipe_catalog/ingredients_list.html'
    ingredients = Ingredient.objects.order_by('name')
    context = {
        'ingredients': ingredients
    }
    return render(request, template_name, context)
