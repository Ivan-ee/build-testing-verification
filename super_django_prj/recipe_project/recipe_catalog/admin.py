from django.contrib import admin
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.utils.html import format_html

# Register your models here.

from .models import Ingredient, Recipe, RecipeIngredient


class IngredientInline(admin.StackedInline):
    """В рецепте есть ингредиенты."""
    model = RecipeIngredient
    extra = 1
    fields = ['ingredient', 'unit', "weight_by_pcs", 'count']


class RecipeAdmin(admin.ModelAdmin):
    """Настройка формы админки для рецепта."""
    inlines = [IngredientInline]
    list_display = ["name", "author", "cooking_time", "total_weight_display", "total_calories_display"]
    readonly_fields = ["author", "image_tag", "total_weight_display", "total_calories_display"]

    def get_queryset(self, request):
        """Ограничивает список объектов только теми, которые созданы текущим пользователем."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def has_change_permission(self, request, obj=None):
        """Запрещает редактирование чужих рецептов."""
        if obj is None:
            return True
        return obj.author == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """Запрещает удаление чужих рецептов."""
        if obj is None:
            return True
        return obj.author == request.user or request.user.is_superuser

    def total_weight_display(self, obj):
        return f"{obj.total_weight()}"

    def total_calories_display(self, obj):
        return f"{obj.total_calories()}"

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    total_weight_display.short_description = "Итоговый вес (грамм)"
    total_calories_display.short_description = "Итоговая калорийность (ккал)"
    image_tag.short_description = "Фотография блюда"


admin.site.register(Recipe, RecipeAdmin)


class IngredientAdmin(admin.ModelAdmin):
    """Настройка формы админки для рецепта."""

    list_display = ["name"]


admin.site.register(Ingredient, IngredientAdmin)
