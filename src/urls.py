from django.urls import path
from .views import (
    base,
    # loginPage,
    page_not_found,
    search_city,
    # register_page,
    query_all_cities,
    fetch_city_suggestions,
)


urlpatterns = [
    path("", base, name="home"),
    # path("login/", loginPage, name="login"),
    path("search/", search_city, name="search"),
    # path("register/", register_page, name="register"),
    path(
        "fetch-city-suggestions/", fetch_city_suggestions, name="fetch_city_suggestions"
    ),
    path("404/", page_not_found, name="404"),
    path("results/", query_all_cities, name="results"),
]
