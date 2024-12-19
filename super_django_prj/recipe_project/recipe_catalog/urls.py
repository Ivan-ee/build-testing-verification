from django.urls import path
from .views import about, index, detail, user_form_test, ingredient, ingredient_edit, ingredient_delete

from django.conf import settings
from django.conf.urls.static import static

app_name = 'recipe_catalog'

urlpatterns = [
                  path('', index, name='home'),
                  path('recipe/<int:pk>/', detail, name='detail'),
                  path('about/', about, name='about'),
                  path('user_form_test/', user_form_test, name='create_user_test'),
                  path('ingredient/', ingredient, name='ingredient'),
                  path('ingredient/<int:pk>/edit/', ingredient_edit, name='ingredient_edit'),
                  path('ingredient/<int:pk>/delete/', ingredient_delete, name='ingredient_delete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
