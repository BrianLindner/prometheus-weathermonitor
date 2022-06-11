"""_summary_

"""
import ast
import configparser
import logging
import time
from typing import Dict, List, Optional, Tuple

from prometheus_client import push_to_gateway  # type: ignore
from prometheus_client import CollectorRegistry, Gauge

from weather.WeatherRegistry import WeatherServiceRegistry
from weather.WeatherService import (
    OpenWeatherMapWeatherService,
    WeatherBitWeatherService,
    WeatherGovWeatherService,
)
from weather.WeatherUtils import TemperatureMeasurement, TemperatureUnit, convert_temperature


def prometheus_temperature(
    registry: CollectorRegistry,
    temperature: TemperatureMeasurement,
    location_name: Optional[str] = None,
    weather_service: Optional[str] = None,
) -> CollectorRegistry:

    namespace = "weather"
    metric = "temperature"
    desc = "Temperature reading from weather service"
    labelnames = ["source", "location"]

    gc = Gauge(
        name=metric,
        documentation=desc,
        labelnames=labelnames,
        unit="celsius",
        registry=registry,
        namespace=namespace,
    )

    gc.labels(weather_service, location_name).set(
        convert_temperature(orig_temperature=temperature, to_unit=TemperatureUnit.CELSIUS).value
    )

    gf = Gauge(
        name=metric,
        documentation=desc,
        labelnames=labelnames,
        unit="fahrenheit",
        registry=registry,
        namespace=namespace,
    )

    gf.labels(weather_service, location_name).set(
        convert_temperature(orig_temperature=temperature, to_unit=TemperatureUnit.FAHRENHEIT).value
    )

    return registry


def push_temperature(
    pushgateway_url: str,
    temperature: TemperatureMeasurement,
    location_name: Optional[str] = None,
    weather_service: Optional[str] = None,
) -> None:
    registry = CollectorRegistry()

    if pushgateway_url is None or pushgateway_url == "":
        raise ValueError("Missing Pushgateway URL")

    registry = prometheus_temperature(
        registry,
        temperature=temperature,
        location_name=location_name,
        weather_service=weather_service,
    )

    push_to_gateway(
        gateway=pushgateway_url,
        job="weather",
        registry=registry,
        grouping_key={"source": weather_service, "location": location_name},
    )


def register_services(
    api_keys: Dict[str, str],
) -> WeatherServiceRegistry:
    registry = WeatherServiceRegistry()

    registry.register_service(
        "weather.gov", WeatherGovWeatherService(api_key=api_keys.get("weather.gov"))  # type: ignore
    )
    registry.register_service(
        "openweathermap", OpenWeatherMapWeatherService(api_key=api_keys.get("openweathermap"))  # type: ignore
    )
    registry.register_service(
        "weatherbit", WeatherBitWeatherService(api_key=api_keys.get("weatherbit"))  # type: ignore
    )

    return registry


def poll_weather_services(
    locations: List[Tuple[str, str]],
    api_keys: Dict[str, str],
    pushgateway_url: str,
    poll_interval: int = 15,
) -> None:

    registry = register_services(api_keys)

    weather_provider = registry.provider

    while True:
        logging.info("Gathering weather forecasts")
        # default wait time between weather lookups
        sleep_minutes = poll_interval

        for l in locations:
            location_code = None

            # grab the location information Dict config
            location_info = l[1]

            # location: Dict[str, str] = json.loads(location_info)
            location = ast.literal_eval(location_info)

            service_name = location["service"]
            location_code = location["location_code"]
            location_name = location["name"]

            weather_service = registry.get_service(service_name)

            try:

                temperature = weather_provider.get_temperature(weather_service, location_code)
                logmsg = f'Weather Service: "{weather_service.name}" Location: "{location_name}" Temp: {convert_temperature(temperature, TemperatureUnit.FAHRENHEIT)}'
                logging.debug(logmsg)

                if temperature:
                    push_temperature(
                        pushgateway_url=pushgateway_url,
                        temperature=temperature,
                        weather_service=service_name,
                        location_name=location_name,
                    )

                else:
                    logmsg = f"no temperature returned - Service: {weather_service} | Location: {location_name}"
                    logging.warning(logmsg)
            except ConnectionRefusedError as cre:
                logmsg = f"get_temperature raised ConnectionRefusedError: {cre}"
                logging.warning(logmsg)
            except ProcessLookupError as ple:
                logmsg = f"get_temperature raised ProcessLookupError: {ple}"
                logging.warning(logmsg)
                # set a retry for the service loop
                logging.warning("retry attempt adjustment")
                sleep_minutes = round(poll_interval / 2, 0)

        # wait to call services again
        logmsg = f"sleeping {sleep_minutes} minutes"
        logging.info(logmsg)
        time.sleep(sleep_minutes * 60)


def main():

    config = configparser.ConfigParser()
    config.read("config.ini")

    required_sections = ["SETTINGS", "API_KEYS", "LOCATIONS"]
    for section in required_sections:
        if not config.has_section(section):
            raise ValueError(f'Missing config param section "[{section}]"')

    # grab and set the log level from the Config
    log_level_str = config["SETTINGS"].get("log_level")

    log_level_info = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "FATAL": logging.FATAL,
    }

    log_level = log_level_info.get(log_level_str, logging.WARNING)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%Y-%m-%d %I:%M:%S %p",
        encoding="utf-8",
    )

    gateway_url = config["SETTINGS"].get("pushgateway")
    poll_interval = config["SETTINGS"].getint("check_interval_minutes")
    locations = config.items("LOCATIONS")
    api_keys = config["API_KEYS"]

    # start the weather monitoring poll service
    poll_weather_services(
        api_keys=api_keys,  # type: ignore
        locations=locations,
        pushgateway_url=gateway_url,
        poll_interval=poll_interval,
    )


if __name__ == "__main__":
    main()
