from dataclasses import dataclass

from lib.colors import Colors
from lib.ui import Positioned, Stack, Text
from screens.base_screen import BaseScreen


@dataclass
class HuckleberryState:
    bottle_ago: str = ""
    sleep_state: str = ""
    sleep_ago: str = ""


class Screen(BaseScreen[HuckleberryState]):
    def __init__(self, bottle_ago="", sleep_state="", sleep_ago=""):
        super().__init__(
            initial_state=HuckleberryState(
                bottle_ago=bottle_ago, sleep_state=sleep_state, sleep_ago=sleep_ago
            )
        )

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

        bottle_label = Text("B: ", font="5x8", color=Colors.white)
        sleep_label = Text("Z: ", font="5x8", color=Colors.white)
        offset = 4
        return Stack(
            children=[
                Positioned(x=offset, y=4, child=bottle_label),
                Positioned(
                    x=offset + bottle_label.width,
                    y=4,
                    child=Text(state.bottle_ago, font="5x8", color=Colors.teal),
                ),
                Positioned(x=offset, y=18, child=sleep_label),
                Positioned(
                    x=offset + sleep_label.width,
                    y=18,
                    child=Text(
                        f"{state.sleep_ago}{' ago' if state.sleep_state == 'active' else ''}",
                        font="5x8",
                        color=Colors.green,
                    ),
                ),
            ]
        )
