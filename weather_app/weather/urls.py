
from django.urls import path
from . import  views
from .views import WeatherData

urlpatterns = [
    # path('', views.index),
    # path('chart/data', views.chart_data),
    path('', WeatherData.as_view())
]