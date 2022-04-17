import random
import time

from lib.colors import COLORS
from lib.fonts import FONTS
from lib.weather import get_current_weather
from PIL import Image
from rgbmatrix import graphics
from screens.base_screen import BaseScreen


class Screen(BaseScreen):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.font = FONTS["5x8"]
        self.white = COLORS["white"]
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()

    def fetch_data_delay(self):
        return 30

    def fetch_data(self):
        weather = get_current_weather()
        feels_like_temp = str(int(weather["main"]["feels_like"]))
        return feels_like_temp

    def render(self):
        self.offscreen_canvas.Clear()
        feels_like_temp = self.get_data()

        if feels_like_temp is not None:
            graphics.DrawText(
                self.offscreen_canvas, self.font, 5, 28, self.white, feels_like_temp + "°"
            )

        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
