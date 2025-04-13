import json
from math import floor
import time
from rgbmatrix import graphics
from screens.base_screen import BaseScreen
from lib.view_helper.text import TextOscillator, right_align_text
from lib.fonts import FONTS
from lib.colors import COLORS


class Screen(BaseScreen):
    def __init__(self, config="{}"):
        super().__init__(display_indefinitely=True)
        self.config = json.loads(config)
        self.font = FONTS["5x8"]
        self.white = COLORS["white"]
        self.rest_duration = 5
        self.is_resting = True
        self.rest_time_start = time.time()
        self.exercises = self.config
        self.exercises_iter = iter(self.exercises)
        self.current_exercise = None
        self.next_exercise()
        self.exercise_start = time.time()
        self.exercise_name_scroller = TextOscillator(
            self.font, self.white, self.font.height, 3
        )

    def animation_interval(self):
        return 1 / 32

    def display_duration(self):
        return super().display_duration()

    def render(self, canvas, data):
        if self.current_exercise is None:
            graphics.DrawText(
                canvas,
                self.font,
                5,
                canvas.height / 2,
                self.white,
                "Done",
            )
            return

        self.exercise_name_scroller.update_text(self.current_exercise["name"])
        self.exercise_name_scroller.render(canvas)

        if self.is_resting:
            graphics.DrawText(
                canvas,
                self.font,
                5,
                canvas.height - self.font.height,
                self.white,
                "in...",
            )

        right_align_text(
            canvas,
            str(self.rest_time_left() if self.is_resting else self.time_left()),
            self.font,
            self.white,
            canvas.height - self.font.height,
            5,
        )

        self.update_state()

    def update_state(self):
        if self.is_resting:
            if self.rest_time_left() <= 0:
                self.is_resting = False
                self.exercise_start = time.time()
        else:
            if self.time_left() <= 0:
                self.next_exercise()
                self.is_resting = True
                self.rest_time_start = time.time()

    def rest_time_left(self):
        return floor(self.rest_duration - (time.time() - self.rest_time_start))

    def time_left(self):
        return floor(
            self.current_exercise["duration"] - (time.time() - self.exercise_start)
        )

    def next_exercise(self):
        self.current_exercise = next(self.exercises_iter, None)
