from django.contrib import admin
from django.utils.html import format_html

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

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

    image_tag.short_description = "Image"

    list_display = ["name", "image_tag"]
    readonly_fields = ["image_tag"]


admin.site.register(Ingredient, IngredientAdmin)
