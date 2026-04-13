import random
from dataclasses import dataclass

from lib.colors import Colors
from lib.fonts import FontRegistry
from lib.ui import Img, Positioned, Stack, Text
from PIL import Image
from screens.base_screen import BaseScreen


@dataclass
class WhoChoosesState:
    rand_int: int = 0


class Screen(BaseScreen[WhoChoosesState]):
    def __init__(self):
        super().__init__(initial_state=WhoChoosesState(rand_int=random.randint(0, 1)))
        self.choices = [
            (Image.open("images/dave.png").convert("RGB"), "DAVE", Colors.green),
            (Image.open("images/nicole.png").convert("RGB"), "NICOLE", Colors.teal),
        ]

    def build(self, state: WhoChoosesState):
        image, name, name_color = self.choices[state.rand_int]
        choose_width = FontRegistry.text_width("5x8", "CHOOSE:")

        return Stack(children=[
            Positioned(x=0, y=0, child=Text("YOU", font="5x8", color=Colors.white)),
            Positioned(x=0, y=8, child=Text("CHOOSE:", font="5x8", color=Colors.white)),
            Positioned(x=0, y=16, child=Text(name, font="5x8", color=name_color)),
            Positioned(x=choose_width + 1, y=0, child=Img(image)),
        ])
