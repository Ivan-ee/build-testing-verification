from django.contrib import admin

# Register your models here.

from .models import Ingredient, Recipe, RecipeIngredient

# admin.site.register(Ingredient)
# admin.site.register(Recipe)


class IngredientInline(admin.StackedInline):
    """В рецепте есть ингредиенты."""
    model = RecipeIngredient
    extra = 5


class RecipeAdmin(admin.ModelAdmin):
    """Настройка формы админки для рецепта."""
    inlines = [IngredientInline]
    list_display = ["name"]


admin.site.register(Recipe, RecipeAdmin)


class IngredientAdmin(admin.ModelAdmin):
    """Настройка формы админки для рецепта."""
    list_display = ["name"]


admin.site.register(Ingredient, IngredientAdmin)
