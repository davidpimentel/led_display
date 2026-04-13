import json
import time
from dataclasses import dataclass
from math import floor
from typing import Optional

from lib.colors import Colors
from lib.fonts import FontRegistry
from lib.ui import AnimatedText, Oscillate, Positioned, Stack, Text
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
        self.exercise_oscillator = Oscillate(font="5x8", delay=3)
        self._next_exercise()

    def setup(self):
        self.run_on_interval(self._tick, seconds=1 / 32)

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

        self.exercise_oscillator.tick()

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

    def build(self, state: StretchingState):
        if state.done:
            return Stack(children=[
                Positioned(x=5, y=12, child=Text("Done", font="5x8", color=Colors.white))
            ])

        if state.current_exercise is None:
            return Stack(children=[])

        children = [
            Positioned(x=0, y=0, child=AnimatedText(state.current_exercise["name"], font="5x8", color=Colors.white, animator=self.exercise_oscillator))
        ]

        if state.is_resting:
            children.append(Positioned(x=5, y=24, child=Text("in...", font="5x8", color=Colors.white)))
            countdown = floor(self.rest_duration - (time.time() - state.rest_time_start))
        else:
            countdown = floor(
                state.current_exercise["duration"] - (time.time() - state.exercise_start)
            )

        countdown_text = str(countdown)
        countdown_width = FontRegistry.text_width("5x8", countdown_text)
        countdown_x = self.width - countdown_width - 5

        children.append(Positioned(x=countdown_x, y=24, child=Text(countdown_text, font="5x8", color=Colors.white)))

        return Stack(children=children)
