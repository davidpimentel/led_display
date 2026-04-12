from dataclasses import dataclass

from lib.colors import Colors
from lib.ui import Offset, Positioned, Scroll, Stack, Text
from screens.base_screen import BaseScreen


@dataclass
class ShowTextState:
    text: str = ""
    scroll_offset: Offset = None


class Screen(BaseScreen[ShowTextState]):
    def __init__(self, text=""):
        super().__init__(initial_state=ShowTextState(text=text))
        self.scroller = Scroll(font="5x8", width=self.width)

    def setup(self):
        self.run_on_interval(self._animate, seconds=1 / 32)

    def _animate(self):
        state = self.get_state()
        self.scroller.set_text(state.text)
        self.set_state(scroll_offset=self.scroller.tick())

    def build(self, state: ShowTextState):
        offset = state.scroll_offset or Offset()
        return Stack(children=[
            Positioned(x=offset.x, y=12, child=Text(state.text, font="5x8", color=Colors.white))
        ])
