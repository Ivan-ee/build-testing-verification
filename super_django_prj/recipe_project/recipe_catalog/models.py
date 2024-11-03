from django.db import models


# Create your models here.

class Ingredient(models.Model):
    """Составная часть рецепта."""
    name = models.CharField(max_length=255)


class Recipe(models.Model):
    """Вкусное делается по рецепту."""
    name = models.CharField(max_length=300)
