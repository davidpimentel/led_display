import json
import subprocess
from dataclasses import dataclass

from lib.colors import COLORS
from lib.fonts import FONTS
from lib.weather import get_current_weather
from PIL import Image
from rgbmatrix import graphics
from screens.base_screen import BaseScreen


@dataclass
class Data:
    people_at_gym: str
    feels_like_temp: str

class Screen(BaseScreen):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.vital_logo = Image.open("./images/vital_logo.png")
        self.font = FONTS["6x9"]
        self.white = COLORS["white"]
        self.green = COLORS["green"]

    def fetch_data_delay(self):
        return 30

    def fetch_data(self):
        people_at_gym = str(
            subprocess.check_output(
                [
                  "curl",
                  "--silent",
                  "https://display.safespace.io/value/live/a7796f34"
                ]
            ).decode("utf-8")
        )
        weather = get_current_weather("40.722518", "-73.954734") # Vital location
        feels_like_temp = str(int(weather["current"]["feels_like"]))
        return Data(
            people_at_gym=people_at_gym,
            feels_like_temp=feels_like_temp
        )

    def get_color_for_range(self, count):
        if count < 100:
            return self.green

    def render(self, data):
        self.offscreen_canvas.Clear()

        if data is not None:
            self.offscreen_canvas.SetImage(
                self.vital_logo.convert("RGB"), offset_x=3, offset_y=3
            )

            graphics.DrawText(
                self.offscreen_canvas, self.font, 8, 28, self.green, data.people_at_gym
            )
            graphics.DrawText(
                self.offscreen_canvas, self.font, 42, 28, self.white, data.feels_like_temp + "°"
            )

        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
