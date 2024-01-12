from django.urls import path
from .views import (
    base,
    loginPage,
    pageNotFound,
    search_city,
    registerPage,
    query_all_cities,
)


urlpatterns = [
    path("", base, name="home"),
    path("login/", loginPage, name="login"),
    path("search/", search_city, name="search"),
    path("register/", registerPage, name="register"),
    path("404/", pageNotFound, name="404"),
    path("results/", query_all_cities, name="results"),
]
