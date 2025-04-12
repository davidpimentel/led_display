import os
import random
import time
from dataclasses import dataclass

from lib.colors import COLORS
from lib.fonts import FONTS
from lib.view_helper.text import TextScroller
from lib.weather import get_current_weather
from PIL import Image
from rgbmatrix import graphics
from screens.base_screen import BaseScreen

SCREEN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


@dataclass
class Data:
    temp: str
    feels_like_temp: str
    description: str
    icon_image: str


class Screen(BaseScreen):
    def __init__(self, lat=None, lon=None):
        super().__init__()
        self.lat = lat
        self.lon = lon
        self.scroll_font = FONTS["5x8"]
        self.temp_font = FONTS["6x12"]
        self.white = COLORS["white"]
        self.gray = COLORS["gray"]
        self.text_scroller = TextScroller(
            font=self.scroll_font, text_color=self.white, position_y=28
        )

    def fetch_data_interval(self):
        return 60

    def animation_interval(self):
        return 0.04

    def fetch_data(self):
        weather = get_current_weather(self.lat, self.lon)
        current_weather = weather["current"]
        temp = str(int(current_weather["temp"])) + "°"
        feels_like_temp = str(int(current_weather["feels_like"])) + "°"

        today_weather_description = current_weather["weather"][0]
        description = today_weather_description["description"].upper()
        icon_id = today_weather_description["icon"]
        icon_image = Image.open(
            SCREEN_DIRECTORY + "/images/" + icon_id + ".png"
        ).convert("RGB")
        return Data(
            temp=temp,
            feels_like_temp=feels_like_temp,
            description=description,
            icon_image=icon_image,
        )

    def render(self, canvas, data):
        if data is not None:
            self.text_scroller.update_text(data.description)
            self.text_scroller.render(canvas)

            canvas.SetImage(data.icon_image, 4, 4)

            hi_temp_len = graphics.DrawText(
                canvas, self.temp_font, 25, 16, self.white, data.temp
            )
            graphics.DrawText(
                canvas,
                self.temp_font,
                28 + hi_temp_len,
                16,
                self.gray,
                data.feels_like_temp,
            )
