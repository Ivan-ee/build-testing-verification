from django.contrib import admin
from django.utils.html import format_html

# Register your models here.

from .models import Ingredient, Recipe, RecipeIngredient


class IngredientInline(admin.StackedInline):
    """В рецепте есть ингредиенты."""
    model = RecipeIngredient
    extra = 1
    fields = ['ingredient', 'count_text', 'count']

    readonly_fields = ['count_text']

    def count_text(self, obj):
        if obj.ingredient.unit:
            unit_label = obj.ingredient.unit.label
            return f"{unit_label}"
        return "Количество в граммах"

    count_text.short_description = "Единица измерения"


class RecipeAdmin(admin.ModelAdmin):
    """Настройка формы админки для рецепта."""
    inlines = [IngredientInline]
    list_display = ["name", "cooking_time", "total_weight_display"]
    readonly_fields = ["total_weight_display"]

    def total_weight_display(self, obj):
        return obj.total_weight()

    # def total_calories_display(self, obj):
    #     return obj.total_calories()

    total_weight_display.short_description = "Итоговый вес (грамм)"
    # total_calories_display.short_description = "Итоговая калорийность (ккал)"


admin.site.register(Recipe, RecipeAdmin)


class IngredientAdmin(admin.ModelAdmin):
    """Настройка формы админки для рецепта."""

    list_display = ["name"]


admin.site.register(Ingredient, IngredientAdmin)
