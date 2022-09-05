from django.shortcuts import render
from django.shortcuts import render, redirect
import requests
from .models import City
from django.contrib import messages 
from datetime import datetime, date
from django.conf import settings
from django.core.mail import send_mail

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

    # send_mail(
    #     'Email Test',
    #     "This mail was sent to test django.core mail services",
    #     settings.EMAIL_HOST_USER,
    #     ['dikepraise119@gmail.com']
    # )
    return render(request,'src/home-view.html',context)
   

def loginPage(request):
    return render(request,'src/login.html')

def pageNotFound(request):
    return render(request,'src/404.html') 