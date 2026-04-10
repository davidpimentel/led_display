from dataclasses import dataclass
from urllib import request

from lib.colors import COLORS
from lib.fonts import FONTS
from lib.weather import get_current_weather
from PIL import Image
from rgbmatrix import graphics
from screens.stateful_screen import StatefulScreen


@dataclass
class GymCountState:
    people_at_gym: str = ""
    feels_like_temp: str = ""


class Screen(StatefulScreen[GymCountState]):
    def __init__(self):
        super().__init__(initial_state=GymCountState())
        self.vital_logo = Image.open("./images/vital_logo.png")
        self.font = FONTS["6x9"]
        self.white = COLORS["white"]
        self.green = COLORS["green"]

    def setup(self):
        self.create_interval(self._fetch_data, seconds=30)

    def _fetch_data(self):
        response = request.urlopen(
            "https://display.safespace.io/value/live/a7796f34", timeout=10
        )
        people_at_gym = response.read().decode("utf-8")
        weather = get_current_weather("40.722518", "-73.954734")  # Vital location
        feels_like_temp = str(int(weather["current"]["feels_like"]))
        self.set_state(
            people_at_gym=people_at_gym,
            feels_like_temp=feels_like_temp,
        )

    def _render(self, canvas, state: GymCountState):
        if not state.people_at_gym:
            return

        canvas.SetImage(
            self.vital_logo.convert("RGB"), offset_x=3, offset_y=3
        )

        graphics.DrawText(
            canvas, self.font, 8, 28, self.green, state.people_at_gym
        )
        graphics.DrawText(
            canvas, self.font, 42, 28, self.white, state.feels_like_temp + "°"
        )
