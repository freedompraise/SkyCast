from django.urls import path
from . import views

urlpatterns = [
    path('',views.base,name='home'),
    path('auth/',views.loginPage, name='login'),
]