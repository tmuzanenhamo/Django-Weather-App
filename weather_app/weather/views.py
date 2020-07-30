from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import date, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
import requests
from . import forms
import json

app_id = "583780f540eb51ffae444cc967d5f6f8"


# Create your views here.


class WeatherData(APIView):
  
    authentication_classes = []
    permission_classes = []
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'weather.html'

    def get(self, request, format=None):
        city_name = forms.City()
        city = ''
        temperature = []
        humidity = []
        return Response({'form': city_name})

    def post(self, request):
        city= ''
        temperature = []
        humidity = []
        tmp = []
        hum = []
        city_name = forms.City()
        today = date.today()
        five_days=date.today() + timedelta(days=5)
        print(five_days)
        if request.method == "POST":
            city_name = forms.City(request.POST)

            if city_name.is_valid():
                print("Data: ")
                print(city_name.cleaned_data['city'])
                city = city_name.cleaned_data['city']
                start_date = city_name.cleaned_data['start']
                end_date = city_name.cleaned_data['end']
                start = f'{start_date} 00:00:00'
                end = f'{end_date} 00:00:00'
                print(end)

                base_url = "http://api.openweathermap.org/data/2.5/forecast"
                complete_url = base_url + "?q=" + city + "&appid=" + app_id
                json_data = requests.get(complete_url).json()
                for item in json_data['list']:
                    time_forecasted = item['dt_txt']
                    if start < time_forecasted < end:
                        temperature.append(item['main']['temp'] - 273.15)
                        humidity.append(item['main']['humidity'])

        def min_temperature(arr):
       
            if len(arr) == 0:
                return 0
            else:
                min_temp = min(arr)
                min_temp = "{:.2f}".format(min_temp)
                tmp.append(float(min_temp))
            return min_temp

        def min_humidity(arr):
            """
                Takes in an array of humidity values, returns the minimum humidity
            """
            if len(arr) == 0:
                return 0
            else:
                min_hum = min(arr)
                min_hum = "{:.2f}".format(min_hum)
                hum.append(float(min_hum))
            return min_hum

        def max_temperature(arr):
            """
                Takes in an array of temperatures, returns the maximum temperature
            """
            if len(arr) == 0:
                return 0
            else:
                max_temp = max(arr)
                max_temp = "{:.2f}".format(max_temp)
                tmp.append(float(max_temp))
            return max_temp

        def max_humidity(arr):
            """
                Takes in an array of humidity values, returns the maximum humidity
            """
            if len(arr) == 0:
                return 0
            else:
                max_hum = max(arr)
                max_hum = "{:.2f}".format(max_hum)
                hum.append(float(max_hum))
            return max_hum

        def average_temperature(arr):
            """
                Takes in an array of temperatures, returns the teperature average
            """
            if len(arr) == 0:
                return 0
            else:
                average_temp = sum(arr) / len(arr)
                average_temp = "{:.2f}".format(average_temp)
                tmp.append(float(average_temp))

            return average_temp

        def average_humidity(arr):
            """
                Takes in an array of humidity values, returns the average humidity
            """
            if len(arr) == 0:
                return 0
            else:
                average_hum = sum(arr) / len(arr)
                average_hum = "{:.2f}".format(average_hum)
                hum.append(float(average_hum))
            return average_hum

        def median_temperature(arr):
            """
                Takes in an array of temperatures, returns the median
            """
            if len(arr) == 0:
                return 0
            else:
                arr.sort()
                mid = len(arr) // 2
                median = (arr[mid] + arr[~mid]) / 2
                median = "{:.2f}".format(median)
                tmp.append(float(median))
            return median

        def median_humidity(arr):
            """
                Takes in an array of humidity values, returns the median
            """
            if len(arr) == 0:
                return 0
            else:
                arr.sort()
                mid = len(arr) // 2
                median = (arr[mid] + arr[~mid]) / 2
                median = "{:.2f}".format(median)
                hum.append(float(median))
            return median

        city_weather = {
        'City': city,
        'Maximum Temperature': max_temperature(temperature),
        'Minimum Temperature': min_temperature(temperature),
        'Maximum Humidity': max_humidity(humidity),
        'Minimum Humidity': min_humidity(humidity),
        'Average Temperature': average_temperature(temperature),
        'Average Humidity': average_humidity(humidity),
        'Median Temperature': median_temperature(temperature),
        'Median Humidity': median_humidity(humidity)
    }
        json_tmp = json.dumps(tmp)
        json_hum = json.dumps(hum)

        context = {'city_weather': city_weather, 'form': city_name, 'temperature':json_tmp, 'humidity': json_hum, 'today': today, 'five_days_later': five_days}

            

        return Response(context)
