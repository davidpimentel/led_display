import os

import requests


def get_current_weather(lat, lon):
    api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")
    response = requests.get(
    f"""https://api.openweathermap.org/data/2.5/onecall?\
lat={lat}&lon={lon}&appid={api_key}&units=imperial"""
    )
    return response.json()
