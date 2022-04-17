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
    def __init__(self, matrix, lat=None, lon=None):
        super().__init__(matrix)
        self.lat = lat
        self.lon = lon
        self.font = FONTS["5x8"]
        self.white = COLORS["white"]
        self.text_scroller = None
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()


    def fetch_data_delay(self):
        return 60

    def animation_delay(self):
        return 0.04

    def fetch_data(self):
        weather = get_current_weather(self.lat, self.lon)
        hi_temp = str(int(weather["main"]["temp_max"])) + "°"
        lo_temp = str(int(weather["main"]["temp_min"])) + "°"
        current_temp = str(int(weather["main"]["temp"])) + "°"
        description = current_temp + "" + weather["weather"][0]["description"].upper()
        icon_id = weather["weather"][0]["icon"]
        icon_image = Image.open(SCREEN_DIRECTORY + "/images/" + icon_id + ".png").convert("RGB")
        return Data(
            hi_temp=hi_temp,
            lo_temp=lo_temp,
            description=description,
            icon_image=icon_image
            )

    def render(self, data):
        self.offscreen_canvas.Clear()

        if data is not None:
            # Replace text scroller if new text
            if self.text_scroller is None or data.description != self.text_scroller.text:
                self.text_scroller = TextScroller(data.description, 5, 28, self.font, self.white)

            self.offscreen_canvas.SetImage(data.icon_image, 4, 4)

            hi_temp_len = graphics.DrawText(
                self.offscreen_canvas, self.font, 25, 13, self.white, data.hi_temp
            )
            graphics.DrawText(
                self.offscreen_canvas, self.font, 29 + hi_temp_len, 13, self.white, data.lo_temp
            )
            self.text_scroller.scroll_text(self.offscreen_canvas)

        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
