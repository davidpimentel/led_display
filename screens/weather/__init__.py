import os
from dataclasses import dataclass

from lib.colors import COLORS
from lib.fonts import FONTS
from lib.view_helper.text import TextScroller
from lib.weather import get_current_weather
from PIL import Image
from rgbmatrix import graphics
from screens.stateful_screen import StatefulScreen

SCREEN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


@dataclass
class WeatherState:
    temp: str = ""
    feels_like_temp: str = ""
    description: str = ""
    icon_image: Image.Image = None


class Screen(StatefulScreen[WeatherState]):
    def __init__(self, lat=None, lon=None):
        super().__init__(initial_state=WeatherState())
        self.lat = lat
        self.lon = lon
        self.scroll_font = FONTS["5x8"]
        self.temp_font = FONTS["6x12"]
        self.white = COLORS["white"]
        self.gray = COLORS["gray"]
        self.text_scroller = TextScroller(
            font=self.scroll_font, text_color=self.white, position_y=28
        )

    def setup(self):
        self.create_interval(self._fetch_weather, seconds=60)
        self.create_interval(self._animate, seconds=0.04)

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
        self.set_state()

    def _render(self, canvas, state: WeatherState):
        if state.icon_image is None:
            return

        self.text_scroller.update_text(state.description)
        self.text_scroller.render(canvas)

        canvas.SetImage(state.icon_image, 4, 4)

        hi_temp_len = graphics.DrawText(
            canvas, self.temp_font, 25, 16, self.white, state.temp
        )
        graphics.DrawText(
            canvas,
            self.temp_font,
            28 + hi_temp_len,
            16,
            self.gray,
            state.feels_like_temp,
        )
