from django.urls import path
from . views import forecast_trend_view

urlpatterns = [
    path("trend/", forecast_trend_view, name="forecast_trend"),
]
