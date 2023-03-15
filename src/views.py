from django.shortcuts import render, redirect
from django.contrib import messages 
from django.conf import settings
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm
from .models import City

import requests
from datetime import datetime

import mailchimp_marketing as MailchimpMarketing

MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER = settings.MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_LIST_ID = settings.MAILCHIMP_EMAIL_LIST_ID


@login_required(login_url='login')
def base(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=816582def5ad0a83096393ac18cf1419'
    city = request.POST.get('city', 'Lagos')
    city_weather = requests.get(url.format(city)).json()

    if city_weather['cod'] == '404':  # conditional when the city queried was found
        return redirect('404')
        
    if City.objects.filter(name=city.lower()).exists() == False:   #to avoid adding a city twice to the database
        City.objects.create(  
            user=request.user,    
            name=city.lower(),
            temp=5/9*(city_weather['main']['temp']-32),
            max=5/9*(city_weather['main']['temp_max']-32),
            min=5/9*(city_weather['main']['temp_min']-32),
         )
    
    context = {
        'city':City.objects.get(name=city.lower() if city is not None else ''), 
        'cities':City.objects.order_by('-time')[:4], # gets the latest three citiess
        'description':city_weather['weather'][0]['description'],
        'humidity': city_weather['main']['humidity'],
        'feels_like': str(5/9*(city_weather['main']['feels_like']-32))[:4],
        'now':datetime.now().strftime("%c"),
        'user':request.user
    }
   
    return render(request,'src/home-view.html',context)


def all_cities(request):
    cities = City.objects.all()
    context = {'cities': cities}
    return render(request, 'src/results.html', context)


def page_not_found(request, exception):
    return render(request,'src/404.html') 


def register(request):
    if request.method == 'POST':        
        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        
        if password == password1:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

            # Add the user to the Mailchimp contact list
            try:
                client = MailchimpMarketing.Client()
                client.set_config({
                    "api_key": MAILCHIMP_API_KEY,
                    "server": MAILCHIMP_DATA_CENTER
                })

                response = client.lists.add_list_member(MAILCHIMP_EMAIL_LIST_ID, {
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
                if user is not None:
                    login(request, user)
                    return redirect('home')

            except Exception as e:
                # Handle any API errors
                print("Error: {}".format(e))
                user.delete()
                messages.error(request, 'Something went wrong. Please try again later.')
        else:
            messages.error(request, 'Invalid form data. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request,'src/register.html')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'src/login.html')
 