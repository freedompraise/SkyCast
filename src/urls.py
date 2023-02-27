from django.urls import path
from . import views

urlpatterns = [
    path('',views.base,name='home'),
    path('auth/',views.loginPage, name='login'),
    path('404/',views.page_not_found, name = "404"),
    path('results/', views.all_cities, name = "cities"),
    path('auth/register/', views.register, name = 'register' ),
]