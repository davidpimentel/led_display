from datetime import datetime

import pytz
from lib.colors import COLORS
from lib.fonts import FONTS
from num2words import num2words
from PIL import Image
from rgbmatrix import graphics
from screens.base_screen import BaseScreen


class Screen(BaseScreen):
    def __init__(self):
        super().__init__(display_indefinitely=True)
        self.timezone = pytz.timezone('US/Eastern')
        self.font = FONTS["6x9"]


    def fetch_data(self):
        return self.get_current_hours_minutes()

    def fetch_data_interval(self):
        return 1

    def get_current_hours_minutes(self):
        current_datetime = datetime.now(tz=self.timezone)
        hour = current_datetime.hour
        if hour == 0:
            hour = 12
        elif hour > 12:
            hour -= 12

        return (hour, current_datetime.minute)

    def hours_minutes_to_words(self, hours_minutes):
        hours, minutes = hours_minutes
        hours_words = num2words(hours)
        minutes_words = num2words(minutes)

        if minutes == 0:
            minutes_words = "o'clock"
        elif minutes < 10:
            minutes_words = "oh " + minutes_words

        minutes_words = minutes_words.replace('-', ' ')
        return (hours_words + " " + minutes_words).upper()

    def render(self, canvas, data):
        current_hours_minutes = data
        self.last_rendered_hours_minutes = current_hours_minutes

        time_in_words = self.hours_minutes_to_words(current_hours_minutes)

        for i, word in enumerate(time_in_words.split(" ")):
            graphics.DrawText(
                canvas,
                self.font,
                3,
                10 + i * 9,
                COLORS["white"],
                word
            )
