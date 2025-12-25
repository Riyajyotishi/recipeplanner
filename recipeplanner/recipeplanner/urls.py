from django.contrib import admin
from django.urls import path
from recipes import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('add/', views.add_recipe, name='add_recipe'),  # ✅ THIS LINE IS MUST
    path('recipe/<int:id>/', views.recipe_detail, name='recipe_detail'),
    path('edit/<int:id>/', views.edit_recipe, name='edit_recipe'),
    path('delete/<int:id>/', views.delete_recipe, name='delete_recipe'),
    path('profile/', views.profile_page, name='profile'),


    path('admin/', admin.site.urls),

      path('', views.recipe_list, name='home'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
     path('logout/', views.logout_page, name='logout'),
]
