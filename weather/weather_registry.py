"""
Registry of available Weather Services (WeatherService objects)

"""
from typing import Protocol

import requests

from weather.weather_service import WeatherServiceProtocol
from weather.weather_utils import (TemperatureMeasurement, TemperatureUnit,
                                   convert_temperature)


class WeatherProviderProtocol(Protocol):
    def get_temperature(
        self, service: WeatherServiceProtocol, location_code: str
    ) -> TemperatureMeasurement:
        ...


class WeatherProvider:
    """Weather Provider

    Processing provider to use various WeatherServiceProtocol services to retrieve and use weather information
    """

    def get_temperature(
        self, service: WeatherServiceProtocol, location_code: str
    ) -> TemperatureMeasurement:

        if service is None:
            raise AttributeError("Weather Service must be provided")

        # retrieve the formatted URL for the Weather Service
        weather_url = service.service_url(location_code=location_code)

        result = requests.get(weather_url)

        # Eval the resonse for issues
        if result.status_code in range(400, 499):
            raise ConnectionRefusedError(f"Error accessing {weather_url} \nResult: {result}")
        elif result.status_code in range(500, 599):
            raise ProcessLookupError(f"Error accessing {weather_url} \nResult: {result}")

        elif result.status_code not in range(200, 399):
            raise ValueError(f"Unable to process result code: {result.status_code}")

        # parse out the temperature value from the overall results
        temperature = service.extract_temperature(result)

        temperature.value = round(temperature.value, 2)

        return temperature

    def get_temperature_celsius(
        self, weather_service: WeatherServiceProtocol, location_code: str
    ) -> TemperatureMeasurement:

        orig_temp = self.get_temperature(weather_service, location_code)
        temperature = convert_temperature(orig_temp, TemperatureUnit.CELSIUS)

        return temperature

    def get_temperature_fahrenheit(
        self, weather_service: WeatherServiceProtocol, location_code: str
    ) -> TemperatureMeasurement:

        orig_temp = self.get_temperature(weather_service, location_code)
        temperature = convert_temperature(orig_temp, TemperatureUnit.FAHRENHEIT)

        return temperature


class WeatherServiceRegistry:
    """Registry of available Weather Services (WeatherService objects)"""

    def __init__(self) -> None:
        self.__services: dict[str, WeatherServiceProtocol] = {}
        self.__provider: WeatherProviderProtocol = WeatherProvider()

    def register_service(self, name: str, service: WeatherServiceProtocol) -> None:
        if self.__services.get(name):
            raise ValueError(f"Weather Service {name} already registered")

        self.__services[name] = service

    def deregister_service(self, name: str) -> None:
        try:
            # self.__services.pop(name)
            del self.__services[name]
        except KeyError:
            pass

    def get_service(self, name: str) -> WeatherServiceProtocol:
        service: WeatherServiceProtocol = self.__services.get(name)  # type: ignore

        if service is None:
            raise ValueError(f"Unknown Weather Service {name}")

        return service

    @property
    def provider(self) -> WeatherProviderProtocol:
        return self.__provider

    @provider.setter
    def provider(self, provider: WeatherProviderProtocol) -> None:
        # method in case in future wish to alter/inject a different provider processor
        self.__provider = provider
