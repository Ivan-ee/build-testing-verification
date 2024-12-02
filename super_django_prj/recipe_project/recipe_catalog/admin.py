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

    def ingredient(self):
        return "Ингредиент"

    def count(self):
        return "Ингредиент"

    ingredient.short_description = "Ингредиент"
    count.short_description = "Количество"
    count_text.short_description = "Единица измерения"


class RecipeAdmin(admin.ModelAdmin):
    """Настройка формы админки для рецепта."""
    inlines = [IngredientInline]
    list_display = ["recipe_name", "recipe_cooking_time", "total_weight_display", "total_calories_display"]
    readonly_fields = ["total_weight_display", "total_calories_display", "image_tag"]

    def recipe_name(self, obj):
        return obj.name

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

    def total_weight_display(self, obj):
        return obj.total_weight()

    def total_calories_display(self, obj):
        return obj.total_calories()

    def recipe_cooking_time(self, obj):
        return obj.cooking_time

    recipe_name.short_description = "Название"
    image_tag.short_description = "Фото"
    recipe_cooking_time.short_description = "Время готовки"
    total_weight_display.short_description = "Итоговый вес (грамм)"
    total_calories_display.short_description = "Итоговая калорийность (ккал)"


admin.site.register(Recipe, RecipeAdmin)


class IngredientAdmin(admin.ModelAdmin):
    """Настройка формы админки для рецепта."""

    list_display = ["name"]


admin.site.register(Ingredient, IngredientAdmin)
