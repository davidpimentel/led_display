from dataclasses import dataclass
from datetime import datetime

import pytz
from lib.colors import Colors
from lib.ui import Positioned, Stack, Text, Padding, Column
from num2words import num2words
from screens.base_screen import BaseScreen


@dataclass
class ClockState:
    hour: int = 0
    minute: int = 0


class Screen(BaseScreen[ClockState]):
    def __init__(self):
        super().__init__(initial_state=ClockState(), display_indefinitely=True)
        self.timezone = pytz.timezone('US/Eastern')

    def setup(self):
        self.run_on_interval(self._fetch_time, seconds=1)

    def _fetch_time(self):
        current_datetime = datetime.now(tz=self.timezone)
        hour = current_datetime.hour
        if hour == 0:
            hour = 12
        elif hour > 12:
            hour -= 12

        self.set_state(hour=hour, minute=current_datetime.minute)

    def _hours_minutes_to_words(self, hour, minute):
        hours_words = num2words(hour)
        minutes_words = num2words(minute)

        if minute == 0:
            minutes_words = "o'clock"
        elif minute < 10:
            minutes_words = "oh " + minutes_words

        minutes_words = minutes_words.replace('-', ' ')
        return (hours_words + " " + minutes_words).upper()

    def build(self, state: ClockState):
        words = self._hours_minutes_to_words(state.hour, state.minute).split(" ")
        return Padding(left=3, top=2, child=Column(children=[
                        Text(w, font="6x9", color=Colors.white)
                for i, w in enumerate(words)
        ])) 
