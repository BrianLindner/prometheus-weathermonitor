"""
Registry of available Weather Sources (WeatherSource objects)

"""
from weather.provider import WeatherProvider, WeatherProviderProtocol
from weather.weathersource import WeatherSourceProtocol

# from weather.weather_utils import TemperatureMeasurement, TemperatureUnit, convert_temperature

weather_factory_source: dict[str, WeatherSourceProtocol] = {}
weather_factory_provider: dict[str, WeatherProviderProtocol] = {}


def register_source(name: str, source: WeatherSourceProtocol) -> None:
    if weather_factory_source.get(name):
        raise ValueError(f"Weather Source {name} already registered")

    weather_factory_source[name] = source


def deregister_source(name: str) -> None:
    try:
        weather_factory_source.pop(name, None)
    except KeyError:
        pass


def source(name: str) -> WeatherSourceProtocol:
    weather_source: WeatherSourceProtocol = weather_factory_source.get(name)  # type: ignore

    if weather_source is None:
        raise ValueError(f"Unknown Weather Source {name}")

    return weather_source


def register_provider(name: str, provider: WeatherProviderProtocol) -> None:
    if name != "default" and weather_factory_provider.get(name):
        raise ValueError(f"Weather Source {name} already registered")

    weather_factory_provider[name] = provider


def deregister_provider(name: str) -> None:
    try:
        weather_factory_provider.pop(name, None)
    except KeyError:
        pass


def provider(name: str = "default") -> WeatherProviderProtocol:
    if name is None:
        return provider("default")

    weather_provider: WeatherProviderProtocol = weather_factory_provider.get(name)  # type: ignore

    # establish the Default provider if was not defined yet
    if name == "default" and weather_provider is None:
        register_provider("default", WeatherProvider())
        return provider("default")

    if weather_provider is None:
        raise ValueError(f'"Unknown Weather Provider "{name}"')

    return weather_provider
