import random

from lib.colors import COLORS
from lib.fonts import FONTS
from screens.base_screen import BaseScreen
from lib.view_helper.text import TextScroller


class Screen(BaseScreen):
    def __init__(self, text=""):
        super().__init__()
        self.font = FONTS["5x8"]
        self.font_height = self.font.height
        self.white = COLORS["white"]
        self.text_scroller = TextScroller(
            font=self.font,
            text_color=self.white,
            position_y=16 + (self.font_height / 2),
        )
        self.text = text
        self.text_scroller.update_text(self.text)

    def animation_interval(self):
        return 1 / 32

    def render(self, canvas, data):
        self.text_scroller.render(canvas)
