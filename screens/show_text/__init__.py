from dataclasses import dataclass

from lib.colors import Colors
from lib.ui import AnimatedText, Positioned, Scroll, Stack
from screens.base_screen import BaseScreen


@dataclass
class ShowTextState:
    text: str = ""


class Screen(BaseScreen[ShowTextState]):
    def __init__(self, text=""):
        super().__init__(initial_state=ShowTextState(text=text))
        self.scroller = Scroll(font="5x8")

    def setup(self):
        self.run_on_interval(self._animate, seconds=1 / 32)

    def _animate(self):
        self.scroller.tick()
        self.set_state()

    def build(self, state: ShowTextState):
        return Stack(children=[
            Positioned(x=0, y=12, child=AnimatedText(state.text, font="5x8", color=Colors.white, animator=self.scroller))
        ])
