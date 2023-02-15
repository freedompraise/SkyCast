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
from datetime import datetime, date
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID

# Create your views here.

def allCities(request):
    context={
        'cities':City.objects.all()
    }
    return render(request, 'src/results.html',context)


@login_required(login_url='login')
def base(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=816582def5ad0a83096393ac18cf1419'
    #if request.method == 'POST':
    city = request.POST.get('city') if request.POST.get('city') else 'Lagos'
    city_weather = requests.get(url.format(city)).json()
    # else:
    #     return redirect('search')
    
    if city_weather['cod'] == '404':  # conditional when the city queried was found
        return redirect('404')
        
       
    if city is not None:
         if City.objects.filter(name = city.lower()).exists() == False :   #to avoid adding a city twice to the database
            City.objects.get_or_create(   
            name = city.lower(),
            temp= 5/9* (city_weather['main']['temp']-32),
            max = 5/9*(city_weather['main']['temp_max']-32),
            min = 5/9*(city_weather['main']['temp_min']-32),
         )
    

    context = {
        'city':City.objects.get(name=city.lower() if city is not None else ''), 
        'cities':City.objects.order_by('-time')[:4], # gets the latest three citiess
        'description':city_weather['weather'][0]['description'],
        'humidity': city_weather['main']['humidity'],
        'feels_like': str(5/9*(city_weather['main']['feels_like']-32))[:4],
        'now':datetime.now().strftime("%c")
    }

   
    return render(request,'src/home-view.html',context)
   


def pageNotFound(request):
    return render(request,'src/404.html') 


def registerPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
             # Subscribe the user to the Mailchimp list
            try:
                client = Client()
                client.set_config({
                    "api_key": settings.MAILCHIMP_API_KEY,
                    "server": "us1"
                })
                client.lists.add_list_member(
                    settings.MAILCHIMP_EMAIL_LIST_ID,
                    {
                        'email_address': user.email,
                        'status': 'subscribed',
                        'merge_fields': {
                            'FNAME': user.username,
                            'LNAME': user.email
                        }
                    }
                )
            except ApiClientError as error:
                # Handle the error
                pass
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request,'src/register.html', {'form':form})


def loginPage(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid username or password.'
    return render(request, 'src/login.html', {'error_message': error_message})

 