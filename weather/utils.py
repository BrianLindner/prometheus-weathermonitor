"""
Utility objects for use with Weather functionality

"""

from dataclasses import dataclass
from enum import Enum
from typing import List


class TemperatureUnit(Enum):
    """Defined enumerated list of Temperature Units to be used for conversion or definition"""

    FAHRENHEIT = "F"
    CELSIUS = "C"
    KELVIN = "K"


@dataclass
class TemperatureMeasurement:
    value: float
    unit: TemperatureUnit

    def __repr__(self) -> str:
        return f"{self.value} {self.unit.value}"


def convert_temperature(
    orig_temperature: TemperatureMeasurement, to_unit: TemperatureUnit
) -> TemperatureMeasurement:
    """Convert temperatures between two units of measure

    Args:
        temperature (float): Temperature to be converted
        from_unit (TemperatureUnit): Conversion from unit of measure (Enum from TemperatureUnit)
        to_unit (TemperatureUnit): Conversion from unit of measure (Enum from TemperatureUnit)

    Raises:
        ValueError: If an invalid/unknown temperature unit is provided for conversion

    Returns:
        float: The converted temerature value in the to_unit unit of measure
    """
    allowed: List[TemperatureUnit] = []
    for entry in TemperatureUnit:
        allowed.append(entry)

    if orig_temperature.unit not in allowed or to_unit not in allowed:
        raise ValueError(
            f'Illegal temperature conversion value: "{orig_temperature.unit}" -> "{to_unit}" Please use {allowed}'
        )

    # nothign to do
    if to_unit == orig_temperature.unit:
        return orig_temperature

    temperature = TemperatureMeasurement(unit=to_unit, value=-99999999)

    if to_unit == TemperatureUnit.CELSIUS:
        if orig_temperature.unit == TemperatureUnit.FAHRENHEIT:
            temperature.value = (orig_temperature.value - 32) / 1.8
        elif orig_temperature.unit == TemperatureUnit.KELVIN:
            temperature.value = orig_temperature.value - 273.15
        else:
            raise ValueError(f"Unable to convert {temperature.unit} to {to_unit}")
    elif to_unit == TemperatureUnit.FAHRENHEIT:
        if orig_temperature.unit == TemperatureUnit.KELVIN:
            temperature.value = (orig_temperature.value * 1.8) - 459.67
        elif orig_temperature.unit == TemperatureUnit.CELSIUS:
            temperature.value = (orig_temperature.value * 1.8) + 32
        else:
            raise ValueError(f"Unable to convert {orig_temperature.value} to {to_unit}")
    elif to_unit == TemperatureUnit.KELVIN:
        if orig_temperature.unit == TemperatureUnit.FAHRENHEIT:
            temperature.value = (orig_temperature.value + 459.67) / 1.8
        elif orig_temperature.unit == TemperatureUnit.CELSIUS:
            temperature.value = orig_temperature.value + 273.15
        else:
            raise ValueError(f"Unable to convert {temperature.unit} to {to_unit}")

    temperature.value = round(temperature.value, 2)

    return temperature


def main():
    """Main function"""
    for entry in TemperatureUnit:
        print(entry)


if __name__ == "__main__":
    main()
