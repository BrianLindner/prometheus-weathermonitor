import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)
sys.path.insert(0, os.path.join(path, "../"))

import pytest
from weather import factory
from weather.provider import WeatherProvider


def test_cant_have_duplicate():

    factory.register_provider("new provider", WeatherProvider())

    with pytest.raises(ValueError):
        factory.register_provider("new provider", WeatherProvider())


def test_replace_default():

    factory.register_provider("default", WeatherProvider())

    try:
        factory.register_provider("default", WeatherProvider())
    except Exception as e:
        pytest.fail(f"DID RAISE {e}")
