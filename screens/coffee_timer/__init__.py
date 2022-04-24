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
        super().__init__()
        self.total_time_in_seconds = total_time_in_seconds
        self.start_time = time.time()
        self.font = FONTS["7x13"]
        self.white = COLORS["white"]
        self.light_brown = graphics.Color(204, 168, 128)
        self.dark_brown = graphics.Color(149, 98, 74)
        self.french_press_img = Image.open(SCREEN_DIRECTORY + "/images/french_press.png").convert("RGB")
        self.bottom_of_press_y = 27
        self.progress_bar_length = 17
        self.blink_text = True

    def fetch_data_delay(self):
        return 1

    def animation_delay(self):
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
        progress_to_fill = int(self.progress_bar_length * data.complete_ratio)

        canvas.SetImage(self.french_press_img, 3, 3)

        for i in range(progress_to_fill):
            color = self.light_brown if i >= progress_to_fill - 2 else self.dark_brown # light brown topper
            y = self.bottom_of_press_y - i
            graphics.DrawLine(canvas, 6, y, 16, y, color)

        if data.complete_ratio >= 1.0:
            if self.blink_text:
                graphics.DrawText(canvas, self.font, 26, 22, self.white, "PLUNGE")

            self.blink_text = not self.blink_text
        else:
            graphics.DrawText(canvas, self.font, 26, 22, self.white, data.time_left)
