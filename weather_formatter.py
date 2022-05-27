from weather_api_service import Weather


def format_weather(weather: Weather) -> str:
    """
    It takes a Weather object and returns a string

    :param weather: Weather - the weather object that contains all the information about the weather
    :type weather: Weather
    :return: A string with the weather in the city.
    """
    return (f"{weather.city}, температура {weather.temperature} °C, {weather.weather_type.value}\n"
            f"Восход: {weather.sunrise.strftime('%H:%M')}\n"
            f"Закат: {weather.sunset.strftime('%H:%M')}\n")


if __name__ == '__main__':
    from datetime import datetime
    from weather_api_service import WeatherType

    print(format_weather(Weather(
        temperature=25,
        weather_type=WeatherType.CLOUDS,
        sunrise=datetime.fromisoformat("2022-05-03 04:00:00"),
        sunset=datetime.fromisoformat("2022-05-03 20:25:00"),
        city="Moscow"
    )))
