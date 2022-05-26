from typing import NamedTuple, TypedDict
from config import USE_ROUNDED_COORDS
import requests

from exceptions import CantGetLocalIP, CantGetLocationInfo


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


class LocalInfo(TypedDict):
    ip: str
    city: str
    region: str
    country: str
    loc: str
    org: str
    postal: str
    timezone: str
    readme: str

def get_coordinates() -> Coordinates:
    """
    It gets the latitude and longitude of the user's location from a website, and returns a Coordinates object with those
    values
    :return: A Coordinates object with the latitude and longitude of the user.
    """
    location_info = _get_local_info()
    latitude, longitude = map(float, location_info["loc"].split(","))
    if USE_ROUNDED_COORDS:
        latitude, longitude = map(lambda x: round(x,1), [latitude, longitude])

    return Coordinates(latitude=latitude,longitude=longitude)


def _get_local_ip() -> str:
    """
    It gets the local IP address of the machine it's running on
    :return: The local IP address of the machine.
    """
    try:
        local_ip = requests.get("https://ifconfig.me").text
    except:
        raise CantGetLocalIP

    return local_ip


def _get_local_info() -> LocalInfo:
    """
    It gets the local IP address, then uses that to get the location info from ipinfo.io
    :return: A dictionary with the following keys:
        ip, hostname, city, region, country, loc, org, postal, timezone, readme
    """
    local_ip = _get_local_ip()
    try:
        location_info = requests.get(f"https://ipinfo.io/{local_ip}").json()
    except:
        raise CantGetLocationInfo

    return location_info



if __name__ == '__main__':
    print(get_coordinates())
