from django.urls import path
from .views import about, index, recipe_detail

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('recipe/<int:pk>/', recipe_detail, name='recipe_detail'),
    path('about/', about, name='about')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
