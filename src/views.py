from django.shortcuts import render
from django.shortcuts import render, redirect
import requests
from .models import City
from django.contrib import messages 
# Create your views here.

def base(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=816582def5ad0a83096393ac18cf1419'
    city = request.POST.get('city')
    api_url = 'https://api.api-ninjas.com/v1/city?name={}'.format(city)
    city_weather = requests.get(url.format(city)).json()
    if city_weather:
        City.objects.create(
            name = city,
            temperature= int(city_weather['main']['temp'])
        )
        
        context = {
        'city':city,
        'cities':City.objects.all(),
        'temperature':city_weather['main']['temp'],
        'description':city_weather['weather'][0]['description'],
        'icon':city_weather['weather'][0]['icon'],
        'max':int(city_weather['main']['temp']) + 4,
        'min':int(city_weather['main']['temp']) - 4,
    }
    else:
        return messages.error(request,'City not found')
   
    return render(request,'src/home-view.html',context)

def loginPage(request):
    return render(request,'src/login.html')