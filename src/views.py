from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm
from .models import City

import requests
from datetime import datetime

import mailchimp_marketing as MailchimpMarketing

api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID
url = settings.OPEN_WEATHER_API_KEY
DEFAULT_CITY = "Lagos"


def get_city_weather(city):
    """Fetches weather data for a given city."""
    return requests.get(url.format(city)).json()


def convert_to_celsius(temp):
    """Converts temperature from Fahrenheit to Celsius."""
    return int(round((temp - 32) * 5 / 9, 2))


def record_city_interest(request, city):
    """Handles city selection actions: adds city to database (if applicable),
    stores it in the session, and retrieves weather data for it."""

    if city:
        city_weather = requests.get(url.format(city)).json()
        city_data = {
            "name": city.lower(),
            "temp": 5 / 9 * (city_weather["main"]["temp"] - 32),
            "time": datetime.now().strftime("%c"),
        }

        if (
            request.user.is_authenticated
            and not City.objects.filter(name=city.lower()).exists()
        ):
            City.objects.create(
                user=request.user,
                name=city_data["name"],
                temp=city_data["temp"],
                max=5 / 9 * (city_weather["main"]["temp_max"] - 32),
                min=5 / 9 * (city_weather["main"]["temp_min"] - 32),
            )

        # Store city in session (for all users)
        queried_cities = request.session.get("queried_cities", [])
        if not any(c["name"] == city_data["name"] for c in queried_cities):
            queried_cities.append(city_data)
            request.session["queried_cities"] = queried_cities


def query_all_cities(request):
    """Queries cities for the current user or session."""
    queried_cities = (
        City.objects.filter(user=request.user).order_by("-time")
        if request.user.is_authenticated
        else request.session.get("queried_cities", [])
    )
    return render(request, "src/results.html", {"cities": queried_cities})


def base(request):
    """Renders the base view with weather data."""
    city = request.session.get("city", DEFAULT_CITY)
    city_weather = get_city_weather(city)
    queried_cities = (
        City.objects.filter(user=request.user).order_by("-time")[:4]
        if request.user.is_authenticated
        else request.session.get("queried_cities", [])
    )

    context = {
        "city": city,
        "cities": queried_cities,
        "description": city_weather["weather"][0]["description"],
        "humidity": city_weather["main"]["humidity"],
        "temp": convert_to_celsius(city_weather["main"]["temp"]),
        "feels_like": convert_to_celsius(city_weather["main"]["feels_like"]),
        "now": datetime.now().strftime("%c"),
        "max": convert_to_celsius(city_weather["main"]["temp_max"]),
        "min": convert_to_celsius(city_weather["main"]["temp_min"]),
        "user": request.user,
    }

    return render(request, "src/base.html", context)


def search_city(request):
    """Handles city search functionality."""
    city = request.POST.get("city", DEFAULT_CITY)
    city_weather = get_city_weather(city)

    if city_weather.get("cod") == "404":
        return redirect("404")

    record_city_interest(request, city)
    request.session["city"] = city

    return redirect("home")


def page_not_found(request):
    """Renders the 404 page."""
    return render(request, "src/404.html")


# def handle_registration_form(email, username, first_name, last_name, password):
#     """Handles user creation and Mailchimp subscription."""
#     try:
#         user, created = User.objects.get_or_create(
#             username=username,
#             email=email,
#             first_name=first_name,
#             last_name=last_name,
#             password=password,
#         )

#         if created:
#             client = MailchimpMarketing.Client()
#             client.set_config({"api_key": api_key, "server": server})
#             client.lists.add_list_member(
#                 list_id,
#                 {
#                     "email_address": email,
#                     "status": "subscribed",
#                     "merge_fields": {
#                         "FNAME": first_name,
#                         "LNAME": last_name,
#                         "USERNAME": username,
#                     },
#                 },
#             )
#         return user, created

#     except Exception as e:
#         User.objects.filter(username=username).delete()
#         raise e


# def register_page(request):
#     """Handles user registration."""
#     if request.method == "POST":
#         email = request.POST.get("email")
#         username = request.POST.get("username")
#         first_name = request.POST.get("first_name")
#         last_name = request.POST.get("last_name")
#         password = request.POST.get("password")
#         password1 = request.POST.get("password1")

#         if password != password1:
#             messages.error(request, "Passwords do not match")
#             return redirect("register")

#         try:
#             user, created = handle_registration_form(
#                 email, username, first_name, last_name, password
#             )

#             if created:
#                 auth_login(request, user)
#                 return redirect("home")
#             else:
#                 messages.error(request, "Username already exists")

#         except Exception as e:
#             messages.error(request, "Technical difficulties. Please try again later.")

#     return render(request, "src/register.html")


# def login_page(request):
#     """Handles user login."""
#     error_message = None
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             auth_login(request, user)
#             return redirect("home")
#         else:
#             error_message = "Invalid username or password."

#     return render(request, "src/login.html", {"error_message": error_message})
