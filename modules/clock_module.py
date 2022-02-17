from datetime import datetime

import pytz
from lib.colors import COLORS
from lib.fonts import FONTS
from num2words import num2words
from PIL import Image
from rgbmatrix import graphics

from .base_module import BaseModule


class ClockModule(BaseModule):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.last_rendered_hours_minutes = None
        self.timezone = pytz.timezone('US/Eastern')
        self.font = FONTS["6x9"]

    def delay_seconds(self):
        return 1

    def get_current_hours_minutes(self):
        current_datetime = datetime.now(tz=self.timezone)
        hour = current_datetime.hour
        if hour > 12:
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

    def render(self):
      current_hours_minutes = self.get_current_hours_minutes()
      if self.last_rendered_hours_minutes == None or self.last_rendered_hours_minutes != current_hours_minutes:
        self.last_rendered_hours_minutes = current_hours_minutes
        self.offscreen_canvas.Clear()

        time_in_words = self.hours_minutes_to_words(current_hours_minutes)

        for i, word in enumerate(time_in_words.split(" ")):
          graphics.DrawText(
              self.offscreen_canvas,
              self.font,
              3,
              10 + i * 9,
              COLORS["white"],
              word
          )

        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
