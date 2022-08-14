from django.shortcuts import render
from django.shortcuts import render, redirect
import requests

def base(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=816582def5ad0a83096393ac18cf1419'
    city = request.POST.get('city')
    api_url = 'https://api.api-ninjas.com/v1/city?name={}'.format(city)
    city_weather = requests.get(url.format(city)).json()
    context = {
        'city':city,
        'temperature':city_weather['main']['temp'],
        'description':city_weather['weather'][0]['description'],
        'icon':city_weather['weather'][0]['icon'],
        'max':int(city_weather['main']['temp']) + 4,
        'min':int(city_weather['main']['temp']) - 4,
    }
    return render(request,'src/home-view.html',context)

def loginPage(request):
    return render(request,'src/login.html')