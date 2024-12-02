from django.urls import path
from .views import about, index, detail

from django.conf import settings
from django.conf.urls.static import static

app_name = 'recipe_catalog'

urlpatterns = [
    path('', index, name='home'),
    path('recipe/<int:pk>/', detail, name='detail'),
    path('about/', about, name='about')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
