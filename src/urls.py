from django.urls import path
from .views import (
    base,
    # loginPage,
    page_not_found,
    search_city,
    # register_page,
    query_all_cities,
)


urlpatterns = [
    path("", base, name="home"),
    # path("login/", loginPage, name="login"),
    path("search/", search_city, name="search"),
    # path("register/", register_page, name="register"),
    path("404/", page_not_found, name="404"),
    path("results/", query_all_cities, name="results"),
]
