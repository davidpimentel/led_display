from dataclasses import dataclass

from screens.stateful_screen import StatefulScreen


@dataclass
class ColorTestState:
    red: int = 255
    green: int = 0
    blue: int = 0


class Screen(StatefulScreen[ColorTestState]):
    def __init__(self):
        super().__init__(initial_state=ColorTestState())

    def setup(self):
        self.create_interval(self._cycle, seconds=3)

    def _cycle(self):
        state = self.get_state()
        self.set_state(red=state.green, green=state.blue, blue=state.red)

    def _render(self, canvas, state: ColorTestState):
        for x in range(0, canvas.width):
            for y in range(0, canvas.height):
                canvas.SetPixel(x, y, state.red, state.green, state.blue)
