from typing import Protocol

import requests

from weather.utils import TemperatureMeasurement, TemperatureUnit, convert_temperature
from weather.weathersource import WeatherSourceProtocol


class WeatherProviderProtocol(Protocol):
    def temperature(
        self, source: WeatherSourceProtocol, location_code: str
    ) -> TemperatureMeasurement:
        ...


class WeatherProvider:
    """Weather Provider

    Processing provider to use various WeatherSourceProtocol sources to retrieve and use weather information
    """

    def temperature(
        self, source: WeatherSourceProtocol, location_code: str
    ) -> TemperatureMeasurement:

        if source is None:
            raise AttributeError("Weather Source must be provided")

        # retrieve the formatted URL for the Weather Source
        weather_url = source.formatted_url(location_code=location_code)

        result = requests.get(weather_url)

        # Eval the resonse for issues
        if result.status_code in range(400, 499):
            raise ConnectionRefusedError(f"Error accessing {weather_url} \nResult: {result}")
        elif result.status_code in range(500, 599):
            raise ProcessLookupError(f"Error accessing {weather_url} \nResult: {result}")

        elif result.status_code not in range(200, 399):
            raise ValueError(f"Unable to process result code: {result.status_code}")

        # parse out the temperature value from the overall results
        temperature = source.extract_temperature(result)

        temperature.value = round(temperature.value, 2)

        return temperature

    def temperature_celsius(
        self, source: WeatherSourceProtocol, location_code: str
    ) -> TemperatureMeasurement:

        orig_temp = self.temperature(source, location_code)
        temperature = convert_temperature(orig_temp, TemperatureUnit.CELSIUS)

        return temperature

    def temperature_fahrenheit(
        self, source: WeatherSourceProtocol, location_code: str
    ) -> TemperatureMeasurement:

        orig_temp = self.temperature(source, location_code)
        temperature = convert_temperature(orig_temp, TemperatureUnit.FAHRENHEIT)

        return temperature
