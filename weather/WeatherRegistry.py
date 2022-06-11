"""
Registry of available Weather Services (WeatherService objects)

"""
import requests

from weather.WeatherService import WeatherServiceProtocol
from weather.WeatherUtils import TemperatureMeasurement, TemperatureUnit, convert_temperature


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
        self._services: dict[str, WeatherServiceProtocol] = {}
        self._provider: WeatherProvider = WeatherProvider()

    def register_service(self, name: str, service: WeatherServiceProtocol) -> None:
        if self._services.get(name):
            raise ValueError(f"Weather Service {name} already registered")

        self._services[name] = service

    def deregister_service(self, name: str) -> None:
        try:
            # self._services.pop(name)
            del self._services[name]
        except KeyError:
            pass

    def get_service(self, name: str) -> WeatherServiceProtocol:
        service: WeatherServiceProtocol = self._services.get(name)  # type: ignore

        if service is None:
            raise ValueError(f"Unknown Weather Service {name}")

        return service

    def get_provider(self) -> WeatherProvider:
        return self._provider
