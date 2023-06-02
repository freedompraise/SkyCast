# Django
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.conf import settings
from django.contrib.auth import authenticate, logout 
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# from src
from .forms import CustomUserCreationForm
from .models import City
# python
import requests
from datetime import datetime, date
# mailchimp
import mailchimp_marketing as MailchimpMarketing


api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID
url = settings.OPEN_WEATHER_API_KEY
DEFAULT_CITY = 'Lagos' # default city to be displayed on the home page

def create_city(city):
    if city is not None:
        if City.objects.filter(name = city.lower()).exists() == False :   #to avoid adding a city twice to the database
            City.objects.get_or_create(  
            user = request.user,    
            name = city.lower(),
            temp= 5/9* (city_weather['main']['temp']-32),
            max = 5/9*(city_weather['main']['temp_max']-32),
            min = 5/9*(city_weather['main']['temp_min']-32),
            )
    
def add_city_to_sessions(city):
    if city:
        if 'queried_cities' not in request.session:
            request.session['queried_cities'] = []  # Initialize an empty list if it doesn't exist yet
            queried_cities = request.session['queried_cities']
            queried_cities.append(city)
            request.session.modified = True  # Save the session after modifying it



@login_required(login_url="login")
def all_cities(request):
    if request.user.is_authenticated:
        queried_cities = City.objects.filter(user = request.user).order_by('-time')[:4]
        
    else:
        queried_cities = request.session.get('queried_cities', [])
    
    context = {
            'cities':queried_cities,
        }
    return render(request, 'src/results.html',context)

def base(request):
    city = request.session.get('city', DEFAULT_CITY)
    city_weather = requests.get(url.format(city)).json()
        
    cities_queried = City.objects.filter(user=request.user).order_by('-time')[:4] if request.user.is_authenticated else None # gets the latest three cities if the user is authenticated
    context = {
        'city':city, 
        'cities':cities_queried, 
        'description':city_weather['weather'][0]['description'],
        'humidity': city_weather['main']['humidity'],
        'temp': str(5/9*(city_weather['main']['temp']-32))[:4],
        'feels_like': str(5/9*(city_weather['main']['feels_like']-32))[:4],
        'now':datetime.now().strftime("%c"),
        'temp': str(5/9*(city_weather['main']['temp']-32))[:4],
        'max': str(5/9*(city_weather['main']['temp_max']-32))[:4],
        'min': str(5/9*(city_weather['main']['temp_min']-32))[:4],
        'user':request.user
    }

    return render(request,'src/base.html',context)

def city_search(request):
    city = request.POST.get('city', DEFAULT_CITY)
    city_weather = requests.get(url.format(city)).json()
    
    if city_weather['cod'] == '404':  # conditional when the city queried was found
        return redirect('404')    
    request.session['city'] = city

    return redirect('home')    

def pageNotFound(request):
    return render(request,'src/404.html') 


def registerPage(request):
    # if the form was sumitted, get the user's input data
    if request.method == 'POST':        
        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        # check if both paswords match
        if password == password1:
            user, created = User.objects.get_or_create(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
        else:
            error_msg = 'Passwords do not match'
            return redirect('register')      

        try:
            # Initialize the Mailchimp SDK
            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": api_key,
                "server": server
            })

            # Add the user to the Mailchimp contact list
            response = client.lists.add_list_member(list_id, {
                "email_address": email,
                "status": "subscribed",
                "merge_fields": {
                "FNAME": first_name,
                "LNAME": last_name,
                "USERNAME": username
                    }
                })
                # Log the response
            print(response)

                 # If the subscriber was added successfully, log the user in and redirect to the home page
            if created:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username already exists')
                return redirect('register')

        except Exception as e:
                # Handle any API errors
                print("Error: {}".format(e))
                messages.error(request,'Sorry. This site is experiencing technical difficulties. Please try again later.')
                User.objects.filter(username=username).delete()
                # if the user mail isn't authenticated, delete from database
                User.objects.filter(username=username).delete()
                
    return render(request,'src/register.html')


def loginPage(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid username or password.'
    return render(request, 'src/login.html', {'error_message': error_message})

 