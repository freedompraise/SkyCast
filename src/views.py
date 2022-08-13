from django.shortcuts import render
from django.shortcuts import render, redirect
# Create your views here.

def base(request):
    return render(request,'src/home-view.html')

def loginPage(request):
    return render(request,'src/login.html')