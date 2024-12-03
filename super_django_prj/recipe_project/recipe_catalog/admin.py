from django.contrib import admin
from django.utils.html import format_html

# Register your models here.

from .models import Ingredient, Recipe, RecipeIngredient


class IngredientInline(admin.StackedInline):
    """В рецепте есть ингредиенты."""
    model = RecipeIngredient
    extra = 1
    fields = ['ingredient', 'unit', "weight_by_pcs", 'count']

    # def count_text(self, obj):
    #     if obj.ingredient.unit:
    #         unit_label = obj.ingredient.unit.label
    #         return f"{unit_label}"
    #     return "Количество в граммах"
    #
    # def ingredient(self):
    #     return "Ингредиент"
    #
    # def count(self):
    #     return "Ингредиент"
    #
    # ingredient.short_description = "Ингредиент"
    # count.short_description = "Количество"
    # count_text.short_description = "Единица измерения"


class RecipeAdmin(admin.ModelAdmin):
    """Настройка формы админки для рецепта."""
    inlines = [IngredientInline]
    list_display = ["name", "cooking_time"]
    readonly_fields = ["image_tag"]

    # def total_weight_display(self, obj):
    #     return f"{obj.total_weight()} г"
    #
    # def total_calories_display(self, obj):
    #     return f"{obj.total_calories()} ккал"

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

    # total_weight_display.short_description = "Итоговый вес"
    # total_calories_display.short_description = "Итоговая калорийность"

    # def recipe_name(self, obj):
    #     return obj.name
    #
    # def image_tag(self, obj):
    #     return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))
    #
    # # def total_weight_display(self, obj):
    # #     return obj.total_weight()
    # #
    # # def total_calories_display(self, obj):
    # #     return obj.total_calories()
    #
    # def recipe_cooking_time(self, obj):
    #     return obj.cooking_time
    #
    # recipe_name.short_description = "Название"
    image_tag.short_description = "Фотография блюда"
    # recipe_cooking_time.short_description = "Время готовки"
    # total_weight_display.short_description = "Итоговый вес (грамм)"
    # total_calories_display.short_description = "Итоговая калорийность (ккал)"


admin.site.register(Recipe, RecipeAdmin)


class IngredientAdmin(admin.ModelAdmin):
    """Настройка формы админки для рецепта."""

    list_display = ["name"]


admin.site.register(Ingredient, IngredientAdmin)
