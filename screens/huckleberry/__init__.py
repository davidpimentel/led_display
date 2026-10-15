from dataclasses import dataclass

from lib.colors import Colors
from lib.ui import Positioned, Stack, Text
from screens.base_screen import BaseScreen


@dataclass
class HuckleberryState:
    bottle_ago: str = ""


class Screen(BaseScreen[HuckleberryState]):
    def __init__(self, bottle_ago=""):
        super().__init__(initial_state=HuckleberryState(bottle_ago=bottle_ago))

    def setup(self):
        self.run_on_interval(self._update_time, seconds=60)

    def _update_time(self):
        # TODO: update display time from timestamp
        pass

    def build(self, state: HuckleberryState):
        if not state.bottle_ago:
            return Stack(
                children=[
                    Positioned(
                        x=24, y=10, child=Text("...", font="5x8", color=Colors.white)
                    )
                ]
            )

        bottle_label = Text("BTL:", font="5x8", color=Colors.white)
        offset = 4
        return Stack(
            children=[
                Positioned(x=offset, y=4, child=bottle_label),
                Positioned(
                    x=offset + bottle_label.width,
                    y=4,
                    child=Text(state.bottle_ago, font="5x8", color=Colors.teal),
                ),
            ]
        )
