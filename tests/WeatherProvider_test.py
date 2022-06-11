import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)
sys.path.insert(0, os.path.join(path, "../"))

import pytest
from weather.WeatherRegistry import WeatherServiceRegistry
from weather.WeatherService import (
    OpenWeatherMapWeatherService,
    WeatherBitWeatherService,
    WeatherGovWeatherService,
)


def test_dup_service():
    registry = WeatherServiceRegistry()

    registry.register_service("weather.gov", WeatherGovWeatherService("abc"))  # type: ignore
    registry.register_service("openweathermap", OpenWeatherMapWeatherService("abc"))  # type: ignore

    with pytest.raises(ValueError):
        registry.register_service("openweathermap", WeatherBitWeatherService("abc"))  # type: ignore
