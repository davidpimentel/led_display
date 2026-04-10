from dataclasses import dataclass

from lib.colors import COLORS
from lib.fonts import FONTS
from lib.view_helper.text import TextScroller
from screens.base_screen import BaseScreen


@dataclass
class ShowTextState:
    text: str = ""


class Screen(BaseScreen[ShowTextState]):
    def __init__(self, text=""):
        super().__init__(initial_state=ShowTextState(text=text))
        self.font = FONTS["5x8"]
        self.font_height = self.font.height
        self.white = COLORS["white"]
        self.text_scroller = TextScroller(
            font=self.font,
            text_color=self.white,
            position_y=16 + (self.font_height / 2),
        )

    def setup(self):
        self.run_on_interval(self._animate, seconds=1 / 32)

    def _animate(self):
        self.set_state()

    def render(self, canvas, state: ShowTextState):
        self.text_scroller.update_text(state.text)
        self.text_scroller.render(canvas)
