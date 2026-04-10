import random
from dataclasses import dataclass

from lib.colors import COLORS
from lib.fonts import FONTS
from PIL import Image
from rgbmatrix import graphics
from screens.stateful_screen import StatefulScreen


@dataclass
class WhoChoosesState:
    rand_int: int = 0


class Screen(StatefulScreen[WhoChoosesState]):
    def __init__(self):
        super().__init__(initial_state=WhoChoosesState(rand_int=random.randint(0, 1)))
        self.font = FONTS["5x8"]
        self.font_height = self.font.height
        self.white = COLORS["white"]
        self.green = COLORS["green"]
        self.teal = COLORS["teal"]
        self.images = [
            (Image.open("images/dave.png").convert("RGB"), "DAVE", self.green),
            (Image.open("images/nicole.png").convert("RGB"), "NICOLE", self.teal),
        ]

    def _render(self, canvas, state: WhoChoosesState):
        image, name, name_color = self.images[state.rand_int]

        graphics.DrawText(
            canvas, self.font, 0, self.font_height, self.white, "YOU"
        )
        length = graphics.DrawText(
            canvas, self.font, 0, (self.font_height * 2), self.white, "CHOOSE:"
        )
        graphics.DrawText(
            canvas, self.font, 0, (self.font_height * 3), name_color, name
        )
        canvas.SetImage(image, length + 1, 0)
