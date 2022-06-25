# import os
# import sys

# path = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, path)
# sys.path.insert(0, os.path.join(path, "../"))

import pytest
from weather import factory
from weather.weathersource import OpenWeatherMapSource, WeatherBitSource, WeatherGovSource


def test_no_dup_service():

    factory.register_source("weather.gov", WeatherGovSource("abc"))
    factory.register_source("openweathermap", OpenWeatherMapSource("abc"))

    with pytest.raises(ValueError):
        factory.register_source("openweathermap", WeatherBitSource("abc"))
