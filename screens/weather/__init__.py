import os
import random
import time
from dataclasses import dataclass

from lib.colors import COLORS
from lib.fonts import FONTS
from lib.view_helper.text import TextScroller, right_align_text
from lib.weather import get_current_weather
from PIL import Image
from rgbmatrix import graphics
from screens.base_screen import BaseScreen

SCREEN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

@dataclass
class Data:
    hi_temp: str
    lo_temp: str
    description: str
    icon_image: str


class Screen(BaseScreen):
    def __init__(self, lat=None, lon=None):
        super().__init__()
        self.lat = lat
        self.lon = lon
        self.font = FONTS["5x8"]
        self.white = COLORS["white"]
        self.text_scroller = None


    def fetch_data_interval(self):
        return 60

    def animation_interval(self):
        return 0.04

    def fetch_data(self):
        weather = get_current_weather(self.lat, self.lon)
        today_weather = weather["daily"][0]
        current_weather = weather["current"]
        hi_temp = str(int(today_weather["temp"]["max"])) + "°"
        lo_temp = str(int(today_weather["temp"]["min"])) + "°"
        current_temp = str(int(current_weather["temp"])) + "°"
        today_weather_description = today_weather["weather"][0]
        description = current_temp + " " + today_weather_description["description"].upper()
        icon_id = today_weather_description["icon"]
        icon_image = Image.open(SCREEN_DIRECTORY + "/images/" + icon_id + ".png").convert("RGB")
        return Data(
            hi_temp=hi_temp,
            lo_temp=lo_temp,
            description=description,
            icon_image=icon_image
            )

    def render(self, canvas, data):
        if data is not None:
            # Replace text scroller if new text
            if self.text_scroller is None or data.description != self.text_scroller.text:
                self.text_scroller = TextScroller(data.description, 5, 28, self.font, self.white)

            canvas.SetImage(data.icon_image, 4, 4)

            hi_temp_len = graphics.DrawText(
                canvas, self.font, 25, 13, self.white, data.hi_temp
            )
            graphics.DrawText(
                canvas, self.font, 29 + hi_temp_len, 13, self.white, data.lo_temp
            )
            self.text_scroller.scroll_text(canvas)
