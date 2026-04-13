import os
from dataclasses import dataclass

from lib.colors import Colors
from lib.fonts import FontRegistry
from lib.ui import AnimatedText, Img, Positioned, Scroll, Stack, Text
from lib.weather import get_current_weather
from PIL import Image
from screens.base_screen import BaseScreen

SCREEN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


@dataclass
class WeatherState:
    temp: str = ""
    feels_like_temp: str = ""
    description: str = ""
    icon_image: Image.Image = None


class Screen(BaseScreen[WeatherState]):
    def __init__(self, lat=None, lon=None):
        super().__init__(initial_state=WeatherState())
        self.lat = lat
        self.lon = lon
        self.scroller = Scroll(font="5x8")

    def setup(self):
        self.run_on_interval(self._fetch_weather, seconds=60)
        self.run_on_interval(self._animate, seconds=0.04)

    def _fetch_weather(self):
        weather = get_current_weather(self.lat, self.lon)
        temp = str(int(weather["main"]["temp"])) + "°"
        feels_like_temp = str(int(weather["main"]["feels_like"])) + "°"

        description = weather["weather"][0]["description"].upper()
        icon_id = weather["weather"][0]["icon"]
        icon_image = Image.open(
            SCREEN_DIRECTORY + "/images/" + icon_id + ".png"
        ).convert("RGB")

        self.set_state(
            temp=temp,
            feels_like_temp=feels_like_temp,
            description=description,
            icon_image=icon_image,
        )

    def _animate(self):
        self.scroller.tick()
        self.set_state()

    def build(self, state: WeatherState):
        if state.icon_image is None:
            return Stack(children=[])

        temp_width = FontRegistry.text_width("6x12", state.temp)

        return Stack(children=[
            Positioned(x=4, y=4, child=Img(state.icon_image)),
            Positioned(x=25, y=4, child=Text(state.temp, font="6x12", color=Colors.white)),
            Positioned(x=28 + temp_width, y=4, child=Text(state.feels_like_temp, font="6x12", color=Colors.gray)),
            Positioned(x=0, y=20, child=AnimatedText(state.description, font="5x8", color=Colors.white, animator=self.scroller)),
        ])
