"""
Weather Services implementing WeatherServiceProtocol functionality to gather weather data
"""

from typing import Protocol

import requests

from weather.weather_utils import TemperatureMeasurement, TemperatureUnit


class WeatherServiceProtocol(Protocol):
    def service_url(self, location_code: str) -> str:
        ...

    def extract_temperature(self, result: requests.Response) -> TemperatureMeasurement:
        ...

    @property
    def name(self) -> str:
        ...


class WeatherGovWeatherService:
    """Weather service class for Weather.gov

    implementation of the WeatherService protocol"""

    def __init__(self, api_key: str) -> None:
        self._name = "Weather.gov"
        self._url_pattern: str = "https://api.weather.gov/gridpoints/{location_code}/forecast"

        # dont really need the API Key, but storing for future just in case
        self.api_key = api_key

    @property
    def name(self) -> str:
        return self._name

    def service_url(self, location_code: str) -> str:
        return self._url_pattern.format(location_code=location_code)

    def extract_temperature(self, result: requests.Response) -> TemperatureMeasurement:
        temperature = result.json()["properties"]["periods"][0]["temperature"]
        temp_unit = result.json()["properties"]["periods"][0]["temperatureUnit"]

        if temp_unit == "F":
            temperatureUnit = TemperatureUnit.FAHRENHEIT
        elif temp_unit == "C":
            temperatureUnit = TemperatureUnit.CELSIUS
        elif temp_unit == "K":
            temperatureUnit = TemperatureUnit.KELVIN
        else:
            raise ValueError(f"Unable to map temperature unit {temp_unit}")

        return TemperatureMeasurement(temperature, temperatureUnit)


class OpenWeatherMapWeatherService:
    """Weather service class for OpenWeatherMap

    implementation of the WeatherService protocol"""

    def __init__(self, api_key: str) -> None:
        self._name = "OpenWeatherMap"
        self._url_pattern: str = (
            "http://api.openweathermap.org/data/2.5/forecast?id={location_code}&appid={api_key}"
        )

        self.api_key = api_key

    @property
    def name(self) -> str:
        return self._name

    def service_url(self, location_code: str) -> str:
        return self._url_pattern.format(location_code=location_code, api_key=self.api_key)

    def extract_temperature(self, result: requests.Response) -> TemperatureMeasurement:
        temperature = result.json()["list"][0]["main"]["temp"]
        temperatureUnit = TemperatureUnit.KELVIN

        return TemperatureMeasurement(temperature, temperatureUnit)


class WeatherBitWeatherService:
    """Weather service class for Weatherbit

    implementation of the WeatherService protocol"""

    def __init__(self, api_key: str) -> None:
        self._name = "Weatherbit"
        self._url_pattern: str = (
            "https://api.weatherbit.io/v2.0/current?city_id={location_code}&key={api_key}"
        )

        self.api_key = api_key

    @property
    def name(self) -> str:
        return self._name

    def service_url(self, location_code: str) -> str:
        return self._url_pattern.format(location_code=location_code, api_key=self.api_key)

    def extract_temperature(self, result: requests.Response) -> TemperatureMeasurement:
        temperature = result.json()["data"][0]["temp"]
        temperatureUnit = TemperatureUnit.CELSIUS

        return TemperatureMeasurement(temperature, temperatureUnit)
