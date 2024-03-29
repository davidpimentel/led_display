import random

from lib.colors import COLORS
from lib.fonts import FONTS
from PIL import Image
from rgbmatrix import graphics
from screens.base_screen import BaseScreen


class Screen(BaseScreen):
    def __init__(self):
        super().__init__()
        self.rand_int = random.randint(0, 1)
        self.font = FONTS["5x8"]
        self.font_height = self.font.height
        self.white = COLORS["white"]
        self.green = COLORS["green"]
        self.teal = COLORS["teal"]

    def render(self, canvas, data):
        images = [
            (Image.open("images/dave.png"), "DAVE", self.green),
            (Image.open("images/nicole.png"), "NICOLE", self.teal),
        ]

        image, name, name_color = images[self.rand_int]

        graphics.DrawText(
            canvas, self.font, 0, self.font_height, self.white, "YOU"
        )
        length = graphics.DrawText(
            canvas, self.font, 0, (self.font_height * 2), self.white, "CHOOSE:"
        )
        graphics.DrawText(
            canvas, self.font, 0, (self.font_height * 3), name_color, name
        )
        canvas.SetImage(image.convert("RGB"), length + 1, 0)
