import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)
sys.path.insert(0, os.path.join(path, "../"))

from weather.weather_utils import TemperatureMeasurement, TemperatureUnit, convert_temperature


def test_convert_C_to_F():
    orig_temp = TemperatureMeasurement(100, TemperatureUnit.CELSIUS)
    new_temp = convert_temperature(orig_temp, TemperatureUnit.FAHRENHEIT)
    assert new_temp.unit == TemperatureUnit.FAHRENHEIT and new_temp.value == 212


def test_convert_C_to_K():
    orig_temp = TemperatureMeasurement(100, TemperatureUnit.CELSIUS)
    new_temp = convert_temperature(orig_temp, TemperatureUnit.KELVIN)
    assert new_temp.unit == TemperatureUnit.KELVIN and new_temp.value == 373.15


def test_convert_F_to_C():
    orig_temp = TemperatureMeasurement(100, TemperatureUnit.FAHRENHEIT)
    new_temp = convert_temperature(orig_temp, TemperatureUnit.CELSIUS)
    assert new_temp.unit == TemperatureUnit.CELSIUS and new_temp.value == 37.78  # 37.7778


def test_convert_F_to_K():
    orig_temp = TemperatureMeasurement(100, TemperatureUnit.FAHRENHEIT)
    new_temp = convert_temperature(orig_temp, TemperatureUnit.KELVIN)
    assert new_temp.unit == TemperatureUnit.KELVIN and new_temp.value == 310.93  # 310.9278


def test_convert_C_to_C():
    orig_temp = TemperatureMeasurement(100, TemperatureUnit.CELSIUS)
    new_temp = convert_temperature(orig_temp, TemperatureUnit.CELSIUS)
    assert new_temp.unit == TemperatureUnit.CELSIUS and new_temp.value == 100


def test_convert_F_to_F():
    orig_temp = TemperatureMeasurement(100, TemperatureUnit.FAHRENHEIT)
    new_temp = convert_temperature(orig_temp, TemperatureUnit.FAHRENHEIT)
    assert new_temp.unit == TemperatureUnit.FAHRENHEIT and new_temp.value == 100


def test_convert_K_to_K():
    orig_temp = TemperatureMeasurement(100, TemperatureUnit.KELVIN)
    new_temp = convert_temperature(orig_temp, TemperatureUnit.KELVIN)
    assert new_temp.unit == TemperatureUnit.KELVIN and new_temp.value == 100
