from django.shortcuts import render
from django.shortcuts import render, redirect
import requests
from .models import City
from django.contrib import messages 
# Create your views here.

def base(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=816582def5ad0a83096393ac18cf1419'
    city = request.POST.get('city')
    city_weather = requests.get(url.format(city)).json()
    if city_weather['cod'] != '404':  # conditional when the city queried was found
        
        if city is not None:
            City.objects.update_or_create(
                name = city,
                temp= (city_weather['main']['temp']),
                max = city_weather['main']['temp_max'],
                min = city_weather['main']['temp_min'],
         )
        
        context = {
        'city':city,
        'cities':City.objects.all(),
        'temperature':city_weather['main']['temp'],
        'description':city_weather['weather'][0]['description'],
        'icon':city_weather['weather'][0]['icon'],
        'max':int(city_weather['main']['temp']) + 4,
        'min':int(city_weather['main']['temp']) - 4,
        'city_data':city_weather,
    }
        return render(request,'src/home-view.html',context)
    else:
        return render(request,'src/404.html')

def loginPage(request):
    return render(request,'src/login.html')