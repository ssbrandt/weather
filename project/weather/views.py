import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
from project.secrets import *
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def index(request):

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=' + WEATHER_API_TOKEN


    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r["main"]['temp'],
            'description': r["weather"][0]["description"],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'weather/weather.html', context)

def signup(request):
    if request.method == 'POST':
        f = SignUpForm(request.POST)
        if f.is_valid():
            f.save()
            username = f.cleaned_data.get('username')
            raw_password = f.cleaned_data.get('password1')
            first_name =f.cleaned_data.get('first_name')
            last_name = f.cleaned_data.get('last_name')
            email = f.cleaned_data.get('email')
            user = authenticate(username=username, password=raw_password)
            return redirect('index')
    else:
        f = SignUpForm()
    return render(request, 'weather/signup.html', {'form': f})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, "weather/login.html", {
                    "message": "Invalid Credentials"
                })
    return render(request, "weather/login.html")

def logout_view(request):
    logout(request)
    return render(request, "weather/weather.html")
