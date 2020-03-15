from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


def index(request):
    cities = City.objects.all()  # return all the cities in the database

    print(f"Cities: {cities}")

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=868c9065b79f5103e61929b03e92a714'

    if request.method == 'POST':  # only true if form is submitted
        form = CityForm(request.POST)  # add actual request data to form for processing
        print(f"form: {form}")
        form.save()  # will validate and save if validate

    form = CityForm()

    weather_data = []

    for city in cities:
        city_weather = requests.get(
            url.format(city)).json()  # request the API data and convert the JSON to Python data types
        print(f"city_weather: {city_weather}")
        if city_weather['cod'] == '404':
            weather = {
                'city': city,
                'temperature': None,
                'description': 'Not Found',
                'icon': None
            }
        else:
            weather = {
                'city': city,
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon']
            }

        weather_data.append(weather)  # add the data for the current city into our list

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'lookup/index.html', context)  # returns the index.html template