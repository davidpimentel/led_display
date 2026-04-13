import os
import time
from dataclasses import dataclass

from lib.colors import Color, Colors
from lib.ui import Img, Positioned, Rect, Stack, Text
from PIL import Image
from screens.base_screen import BaseScreen

SCREEN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

LIGHT_BROWN = Color(204, 168, 128)
DARK_BROWN = Color(149, 98, 74)
BOTTOM_OF_PRESS_Y = 27
PROGRESS_BAR_LENGTH = 17
PROGRESS_BAR_WIDTH = 11


@dataclass
class CoffeeTimerState:
    time_left: str = "04:00"
    complete_ratio: float = 0.0
    completed_animation_counter: int = 0


class Screen(BaseScreen[CoffeeTimerState]):
    def __init__(self, total_time_in_seconds=240):
        super().__init__(
            initial_state=CoffeeTimerState(),
            duration=(total_time_in_seconds + 30),
        )
        self.total_time_in_seconds = total_time_in_seconds
        self.start_time = time.time()
        self.french_press_img = Image.open(SCREEN_DIRECTORY + "/images/french_press.png").convert("RGB")

    def setup(self):
        self.run_on_interval(self._tick, seconds=1)

    def _tick(self):
        elapsed_seconds = time.time() - self.start_time
        time_left_seconds = max(0, self.total_time_in_seconds - elapsed_seconds)
        time_left = time.strftime("%M:%S", time.gmtime(time_left_seconds))
        complete_ratio = min((elapsed_seconds / self.total_time_in_seconds), 1.0)

        state = self.get_state()
        counter = state.completed_animation_counter + 1 if complete_ratio >= 1.0 else 0

        self.set_state(
            time_left=time_left,
            complete_ratio=complete_ratio,
            completed_animation_counter=counter,
        )

    def build(self, state: CoffeeTimerState):
        children = [Positioned(x=3, y=3, child=Img(self.french_press_img))]

        if state.complete_ratio < 1.0:
            progress_to_fill = int(PROGRESS_BAR_LENGTH * state.complete_ratio)
            children.append(Positioned(x=26, y=9, child=Text(state.time_left, font="7x13", color=Colors.white)))
        else:
            progress_to_fill = int(PROGRESS_BAR_LENGTH - (PROGRESS_BAR_LENGTH * (.25 * (state.completed_animation_counter % 5))))
            if progress_to_fill < 0:
                progress_to_fill = PROGRESS_BAR_LENGTH
            children.append(Positioned(x=26, y=10, child=Text("PLUNGE", font="6x12", color=Colors.white)))

        if progress_to_fill > 0:
            light_height = min(2, progress_to_fill)
            dark_height = max(0, progress_to_fill - 2)
            top_y = BOTTOM_OF_PRESS_Y - progress_to_fill + 1

            children.append(Positioned(x=6, y=top_y, child=Rect(PROGRESS_BAR_WIDTH, light_height, color=LIGHT_BROWN)))
            if dark_height > 0:
                children.append(Positioned(x=6, y=top_y + light_height, child=Rect(PROGRESS_BAR_WIDTH, dark_height, color=DARK_BROWN)))

        return Stack(children=children)
