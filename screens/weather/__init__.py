import random
import time
from dataclasses import dataclass

from lib.colors import COLORS
from lib.fonts import FONTS
from lib.view_helper.text import right_align_text
from lib.weather import get_current_weather
from PIL import Image
from rgbmatrix import graphics
from screens.base_screen import BaseScreen


@dataclass
class Data:
    day_of_week: str
    date: str
    temp: str
    feels_like: str


class Screen(BaseScreen):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.font = FONTS["5x8"]
        self.white = COLORS["white"]
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()

    def fetch_data_delay(self):
        return 5

    def fetch_data(self):
        day_of_week = "THU"
        date = "FEB14"
        weather = get_current_weather()
        temp = str(int(weather["main"]["temp"])) + "°"
        feels_like = str(int(weather["main"]["feels_like"])) + "°"
        return Data(day_of_week=day_of_week, date=date, temp=temp, feels_like=feels_like)

    def render(self, data):
        self.offscreen_canvas.Clear()

        if data is not None:
            graphics.DrawText(
                self.offscreen_canvas, self.font, 5, 20, self.white, data.day_of_week
            )
            graphics.DrawText(
                self.offscreen_canvas, self.font, 5, 28, self.white, data.date
            )
            right_align_text(
                canvas=self.offscreen_canvas,
                text=data.temp,
                font=self.font,
                font_color=self.white,
                y=20
            )
            right_align_text(
                canvas=self.offscreen_canvas,
                text=data.feels_like,
                font=self.font,
                font_color=self.white,
                y=28
            )


        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
