from django.contrib.auth import views
from django.contrib.auth.forms import UserCreationForm
from django.urls import path, reverse_lazy
from django.views.generic import CreateView

from .models import User
from .views import about, index, detail, ingredient, ingredient_edit, ingredient_delete, recipe_create, \
    recipe_edit, recipe_delete, my_recipes

from django.conf import settings
from django.conf.urls.static import static

app_name = 'recipe_catalog'

urlpatterns = [
                  path('', index, name='home'),
                  path('recipe/<int:pk>/', detail, name='detail'),
                  path('about/', about, name='about'),
                  path('ingredient/', ingredient, name='ingredient'),
                  path('ingredient/<int:pk>/edit/', ingredient_edit, name='ingredient_edit'),
                  path('ingredient/<int:pk>/delete/', ingredient_delete, name='ingredient_delete'),

                  path('recipe/', recipe_create, name='recipe_create'),
                  path('recipe/<int:pk>/edit/', recipe_edit, name='recipe_edit'),
                  path('recipe/<int:pk>/delete/', recipe_delete, name='recipe_delete'),

                  path('my_recipes/', my_recipes, name='my_recipes'),

                  path('auth/login/', views.LoginView.as_view(template_name='login.html'), name='login'),
                  path('auth/register/', CreateView.as_view(
                      template_name='register.html',
                      model=User,
                      form_class=UserCreationForm,
                      success_url=reverse_lazy('recipe_catalog:home')
                  ), name='register'),
                  path('auth/logout/', views.LogoutView.as_view(), name='logout'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
