from django.contrib import admin
from django.utils.html import format_html

# Register your models here.

from .models import Ingredient, Recipe, RecipeIngredient


class IngredientInline(admin.StackedInline):
    """В рецепте есть ингредиенты."""
    model = RecipeIngredient
    extra = 1
    fields = ['ingredient', 'weight']


class RecipeAdmin(admin.ModelAdmin):
    """Настройка формы админки для рецепта."""
    inlines = [IngredientInline]
    list_display = ["name", "cooking_time", "total_weight_display", "total_calories_display"]
    readonly_fields = ["total_weight_display", "total_calories_display"]

    def total_weight_display(self, obj):
        return obj.total_weight()

    def total_calories_display(self, obj):
        return obj.total_calories()

    total_weight_display.short_description = "Итоговый вес (грамм)"
    total_calories_display.short_description = "Итоговая калорийность (ккал)"


admin.site.register(Recipe, RecipeAdmin)


class IngredientAdmin(admin.ModelAdmin):
    """Настройка формы админки для рецепта."""

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

    image_tag.short_description = "Image"

    list_display = ["name", "calories", "image_tag"]
    readonly_fields = ["image_tag"]


admin.site.register(Ingredient, IngredientAdmin)
