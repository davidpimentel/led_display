import json
import time
from dataclasses import dataclass, field
from math import floor
from typing import Optional

from lib.colors import COLORS
from lib.fonts import FONTS
from lib.view_helper.text import TextOscillator, right_align_text
from rgbmatrix import graphics
from screens.base_screen import BaseScreen


@dataclass
class StretchingState:
    current_exercise: Optional[dict] = None
    is_resting: bool = True
    rest_time_start: float = 0.0
    exercise_start: float = 0.0
    done: bool = False


class Screen(BaseScreen[StretchingState]):
    def __init__(self, config="{}"):
        super().__init__(
            initial_state=StretchingState(rest_time_start=time.time()),
            display_indefinitely=True,
        )
        self.rest_duration = 5
        self.exercises_iter = iter(json.loads(config))
        self.font = FONTS["5x8"]
        self.white = COLORS["white"]
        self.exercise_name_scroller = TextOscillator(
            self.font, self.white, self.font.height, 3
        )
        self._next_exercise()

    def setup(self):
        self.create_interval(self._tick, seconds=1 / 32)

    def _next_exercise(self):
        exercise = next(self.exercises_iter, None)
        if exercise is None:
            self.set_state(done=True, current_exercise=None)
        else:
            self.set_state(current_exercise=exercise)

    def _tick(self):
        state = self.get_state()
        if state.done:
            return

        if state.is_resting:
            rest_left = floor(self.rest_duration - (time.time() - state.rest_time_start))
            if rest_left <= 0:
                self.set_state(is_resting=False, exercise_start=time.time())
            else:
                self.set_state()
        else:
            time_left = floor(
                state.current_exercise["duration"] - (time.time() - state.exercise_start)
            )
            if time_left <= 0:
                self._next_exercise()
                self.set_state(is_resting=True, rest_time_start=time.time())
            else:
                self.set_state()

    def render(self, canvas, state: StretchingState):
        if state.done:
            graphics.DrawText(
                canvas,
                self.font,
                5,
                canvas.height / 2,
                self.white,
                "Done",
            )
            return

        if state.current_exercise is None:
            return

        self.exercise_name_scroller.update_text(state.current_exercise["name"])
        self.exercise_name_scroller.render(canvas)

        if state.is_resting:
            graphics.DrawText(
                canvas,
                self.font,
                5,
                canvas.height - self.font.height,
                self.white,
                "in...",
            )
            countdown = floor(self.rest_duration - (time.time() - state.rest_time_start))
        else:
            countdown = floor(
                state.current_exercise["duration"] - (time.time() - state.exercise_start)
            )

        right_align_text(
            canvas,
            str(countdown),
            self.font,
            self.white,
            canvas.height - self.font.height,
            5,
        )
