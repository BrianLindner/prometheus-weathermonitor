import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)
sys.path.insert(0, os.path.join(path, "../"))

import pytest
from weather import factory
from weather.weathersource import (
    OpenWeatherMapWeatherSource,
    WeatherBitWeatherSource,
    WeatherGovWeatherSource,
)


def test_dup_service():

    factory.register_source("weather.gov", WeatherGovWeatherSource("abc"))
    factory.register_source("openweathermap", OpenWeatherMapWeatherSource("abc"))

    with pytest.raises(ValueError):
        factory.register_source("openweathermap", WeatherBitWeatherSource("abc"))
