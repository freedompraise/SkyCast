from django.shortcuts import render
from django.shortcuts import render, redirect
import requests
from .models import City
from django.contrib import messages 
from datetime import datetime, date

# Create your views here.

def search(request):
    if request.method == 'POST':
        return redirect('home')
    return render(request, 'src/search.html')



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
    else:
        return redirect('search')
    

    context = {
        'city':City.objects.get(name=city.lower() if city is not None else ''),
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