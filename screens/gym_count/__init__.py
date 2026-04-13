from dataclasses import dataclass
from urllib import request

from lib.colors import Colors
from lib.ui import Img, Positioned, Stack, Text
from lib.weather import get_current_weather
from PIL import Image
from screens.base_screen import BaseScreen


@dataclass
class GymCountState:
    people_at_gym: str = ""
    feels_like_temp: str = ""


class Screen(BaseScreen[GymCountState]):
    def __init__(self):
        super().__init__(initial_state=GymCountState())
        self.vital_logo = Image.open("./images/vital_logo.png").convert("RGB")

    def setup(self):
        self.run_on_interval(self._fetch_data, seconds=30)

    def _fetch_data(self):
        response = request.urlopen(
            "https://display.safespace.io/value/live/a7796f34", timeout=10
        )
        people_at_gym = response.read().decode("utf-8")
        weather = get_current_weather("40.722518", "-73.954734")  # Vital location
        feels_like_temp = str(int(weather["main"]["feels_like"]))
        self.set_state(
            people_at_gym=people_at_gym,
            feels_like_temp=feels_like_temp,
        )

    def build(self, state: GymCountState):
        if not state.people_at_gym:
            return Stack(children=[])

        return Stack(children=[
            Positioned(x=3, y=3, child=Img(self.vital_logo)),
            Positioned(x=8, y=19, child=Text(state.people_at_gym, font="6x9", color=Colors.green)),
            Positioned(x=42, y=19, child=Text(state.feels_like_temp + "°", font="6x9", color=Colors.white)),
        ])
