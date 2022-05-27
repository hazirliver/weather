from datetime import datetime
from enum import Enum
from typing import NamedTuple, Literal
import json
from json.decoder import JSONDecodeError

import requests

from coordinates import Coordinates
import config
from exceptions import ApiServiceError

Celsius = int


class WeatherType(Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморозь"
    RAIN = "Дождь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Облачно"


class Weather(NamedTuple):
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordinates: Coordinates) -> Weather:
    """
    It takes a set of coordinates and returns the weather at that location

    :param coordinates: Coordinates
    :type coordinates: Coordinates
    :return: Weather
    """
    openweather_response = _get_openweather_response(longitude=coordinates.longitude, latitude=coordinates.latitude)
    return _parse_openweather_response(openweather_response)


def _get_openweather_response(latitude: float, longitude: float) -> str:
    """
    It takes a latitude and longitude and returns the response from the OpenWeather API

    :param latitude: float
    :type latitude: float
    :param longitude: float
    :type longitude: float
    :return: A string of the response from the OpenWeather API.
    """
    url = config.OPENWEATHER_URL.format(latitude=latitude, longitude=longitude)
    try:
        return requests.get(url).text
    except requests.exceptions.RequestException:
        raise ApiServiceError


def _parse_openweather_response(openweather_response: str) -> Weather:
    """
    It takes a JSON string and returns a Weather object

    :param openweather_response: str - the response from the OpenWeather API
    :type openweather_response: str
    :return: A Weather object
    """
    try:
        openweather_dict = json.loads(openweather_response)
    except JSONDecodeError:
        raise ApiServiceError

    return Weather(
        temperature=_parse_temperature(openweather_dict),
        weather_type=_parse_weather_type(openweather_dict),
        sunrise=_parse_sun_time(openweather_dict, "sunrise"),
        sunset=_parse_sun_time(openweather_dict, "sunset"),
        city=_parse_city(openweather_dict)
    )


def _parse_temperature(openweather_dict: dict) -> Celsius:
    """
    It takes a openweather_dict dictionary, and returns a temperature in Celsius

    :param openweather_dict: The dictionary returned by the OpenWeatherMap API
    :type openweather_dict: dict
    :return: The temperature in Celsius.
    """
    return round(openweather_dict["main"]["temp"])


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    """
    It takes a dictionary from the OpenWeather API and returns a `WeatherType` enum

    :param openweather_dict: The dictionary returned by the OpenWeatherMap API
    :type openweather_dict: dict
    :return: A WeatherType object
    """
    try:
        weather_type_id = str(openweather_dict["weather"][0]["id"])
    except (IndexError, KeyError):
        raise ApiServiceError

    weather_types = {
        "1": WeatherType.THUNDERSTORM,
        "3": WeatherType.DRIZZLE,
        "5": WeatherType.RAIN,
        "6": WeatherType.SNOW,
        "7": WeatherType.FOG,
        "800": WeatherType.CLEAR,
        "80": WeatherType.CLOUDS,
    }

    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type

    raise ApiServiceError


def _parse_sun_time(
        openweather_dict: dict,
        time: Literal["sunrise"] | Literal["sunset"]) -> datetime:
    """
        It takes a dictionary
        containing the OpenWeather API response, and a string indicating whether
        we want the sunrise or sunset time, and returns a datetime object
        representing the time

        :param openweather_dict: The dictionary returned by the OpenWeatherMap API
        :type openweather_dict: dict
        :param time: Literal["sunrise"] | Literal["sunset"]
        :type time: Literal["sunrise"] | Literal["sunset"]
        :return: A datetime object.
        """
    return datetime.fromtimestamp(openweather_dict["sys"][time])


def _parse_city(openweather_dict: dict) -> str:
    """
    It takes a dictionary that represents the JSON response from OpenWeatherMap, and returns the name of the city

    :param openweather_dict: The dictionary returned by the OpenWeatherMap API
    :type openweather_dict: dict
    :return: The city name.
    """
    return openweather_dict["name"]


if __name__ == '__main__':
    print(get_weather(Coordinates(40.8046, 44.4939)))
