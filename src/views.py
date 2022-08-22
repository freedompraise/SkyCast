from django.shortcuts import render
from django.shortcuts import render, redirect
import requests
from .models import City
from django.contrib import messages 
from datetime import datetime, date

# Create your views here.

def base(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=816582def5ad0a83096393ac18cf1419'
    page = 'search'
    if request.method == 'POST':
        page= 'display'
    city = request.POST.get('city')
    city_weather = requests.get(url.format(city)).json()
    if city_weather['cod'] == '404':  # conditional when the city queried was found
        return redirect('404')
        
       
    if city is not None:
        City.objects.get_or_create(
            name = city,
            temp= (city_weather['main']['temp']),
            max = city_weather['main']['temp_max'],
            min = city_weather['main']['temp_min'],
        )
    context = {
        'city':City.objects.filter(name=city),
        'cities':City.objects.all()[:4],
        'description':city_weather['weather'][0]['description'],
        'feels_like': city_weather['main']['feels_like'],
        'now':datetime.now().strftime("%c")
    }
    return render(request,'src/home-view.html',context)

def loginPage(request):
    return render(request,'src/login.html')

def pageNotFound(request):
    return render(request,'src/404.html') 