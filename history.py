from datetime import datetime
from pathlib import Path
from typing import Protocol, TypedDict
import json

from weather_api_service import Weather
from weather_formatter import format_weather


class HistoryRecord(TypedDict):
    date: str
    weather: str


class WeatherStorage(Protocol):
    """Interface for any storage saving weather"""

    def save(self, weather: Weather) -> None:
        raise NotImplementedError


class PlainFileWeatherStorage:
    """Store weather in plain text file"""

    def __init__(self, file: Path):
        self._file = file

    def save(self, weather: Weather) -> None:
        """
        It opens the file in append mode, writes the current time and the formatted weather to the file, and then closes the
        file

        :param weather: Weather - the weather object that we want to save
        :type weather: Weather
        """
        now = datetime.now()
        formatted_weather = format_weather(weather)
        with open(self._file, "a") as f:
            f.write(f"{now}\n{formatted_weather}\n")


class JSONFileWeatherStorage(WeatherStorage):
    """Store weather in JSON file"""

    def __init__(self, jsonfile: Path):
        self._jsonfile = jsonfile
        self._init_storage()

    def save(self, weather: Weather) -> None:
        """
        It reads the history from the file, appends the new weather to it, and writes it back to the file

        :param weather: Weather
        :type weather: Weather
        """
        history = self._read_history()
        history.append({
            "date": str(datetime.now()),
            "weather": format_weather(weather)
        })
        self._write(history)

    def _init_storage(self) -> None:
        """
        If the file doesn't exist, create it and write an empty list to it
        """
        if not self._jsonfile.exists():
            self._jsonfile.write_text("[]")

    def _read_history(self) -> list[HistoryRecord]:
        """
        It reads the history from a file
        :return: A list of HistoryRecord objects.
        """
        with open(self._jsonfile, "r") as f:
            return json.load(f)

    def _write(self, history: list[HistoryRecord]) -> None:
        """
        > This function writes the history to a json file

        :param history: list[HistoryRecord]
        :type history: list[HistoryRecord]
        """
        with open(self._jsonfile, "w") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)


def save_weather(weather: Weather, storage: WeatherStorage) -> None:
    """
    It saves a weather object to a storage object

    :param weather: Weather
    :type weather: Weather
    :param storage: WeatherStorage - the storage to save the weather to
    :type storage: WeatherStorage
    """
    storage.save(weather=weather)
