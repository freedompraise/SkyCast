from django.urls import path
from . import views, weatherViews


urlpatterns = [
    path('',views.base,name='home'),
    path('search/',views.search_city,name='search'),
    path('auth/',views.loginPage, name='login'),
    path('404/',views.pageNotFound, name = "404"),
    path('results/', views.query_all_cities, name = "cities"),
    path('auth/register/', views.registerPage, name = 'register' ),
    # path('city/<int:city_id>/climate-change/', weatherViews.ClimateChangeView(), name = 'climate_change'),
]