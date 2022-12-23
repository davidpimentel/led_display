import os
import time
from dataclasses import dataclass

from lib.colors import COLORS
from lib.fonts import FONTS
from PIL import Image
from rgbmatrix import graphics
from screens.base_screen import BaseScreen

SCREEN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

@dataclass
class Data:
    time_left: str
    complete_ratio: float


class Screen(BaseScreen):
    def __init__(self, total_time_in_seconds=240):
        super().__init__(duration=(total_time_in_seconds + 30))
        self.total_time_in_seconds = total_time_in_seconds
        self.start_time = time.time()
        self.number_font = FONTS["7x13"]
        self.plunge_font = FONTS["6x12"]
        self.white = COLORS["white"]
        self.light_brown = graphics.Color(204, 168, 128)
        self.dark_brown = graphics.Color(149, 98, 74)
        self.french_press_img = Image.open(SCREEN_DIRECTORY + "/images/french_press.png").convert("RGB")
        self.bottom_of_press_y = 27
        self.progress_bar_length = 17
        self.completed_animation_counter = 0

    def fetch_data_interval(self):
        return 1

    def animation_interval(self):
        return 1

    def fetch_data(self):
        elapsed_seconds = time.time() - self.start_time
        time_left_seconds = self.total_time_in_seconds - elapsed_seconds
        time_left_seconds = 0 if time_left_seconds <= 0 else time_left_seconds
        time_left = time.strftime("%M:%S", time.gmtime(time_left_seconds))
        complete_ratio = min((elapsed_seconds / self.total_time_in_seconds), 1.0)
        return Data(
            time_left=time_left,
            complete_ratio=complete_ratio
        )

    def render(self, canvas, data):
        # French press outline
        canvas.SetImage(self.french_press_img, 3, 3)

        # french press fill level
        if data.complete_ratio < 1.0:
            progress_to_fill = int(self.progress_bar_length * data.complete_ratio)
            graphics.DrawText(canvas, self.number_font, 26, 22, self.white, data.time_left)
        else:
            graphics.DrawText(canvas, self.plunge_font, 26, 22, self.white, "PLUNGE")

            progress_to_fill = int(self.progress_bar_length - (self.progress_bar_length * (.25 * (self.completed_animation_counter % 5))))
            if progress_to_fill < 0:
                progress_to_fill = self.progress_bar_length

            self.completed_animation_counter += 1


        # fill in coffee progress
        for i in range(progress_to_fill):
            color = self.light_brown if i >= progress_to_fill - 2 else self.dark_brown # light brown topper
            y = self.bottom_of_press_y - i
            graphics.DrawLine(canvas, 6, y, 16, y, color)
