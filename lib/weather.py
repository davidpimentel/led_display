import os

import requests


def get_current_weather():
  api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")
  response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Brooklyn&appid={0}&units=imperial".format(api_key))
  return response.json()
