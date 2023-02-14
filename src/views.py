from django.shortcuts import render, redirect
from django.contrib import messages 
from django.conf import settings
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User


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


# Subscription Logic
def subscribe(email):
    """
     Contains code handling the communication to the mailchimp api
     to create a contact/member in an audience/list.
    """

    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })

    member_info = {
        "email_address": email,
        "status": "subscribed",
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occured: {}".format(error.text))



def registerPage(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, email = email, password = password)
    if user is None:
        User.objects.create(email=email, password=password)


def loginPage(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, email = email, password = password)
    if user is not None:
        login(request,user)
        subscribe(email)
        return redirect(home)
    else:
        messages.error((request), "You failed the test!")

    return render(request,'src/login.html')

 