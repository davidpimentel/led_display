import time
import math
from dataclasses import dataclass

from lib.fonts import FontRegistry


@dataclass
class Offset:
    x: int = 0
    y: int = 0


class Scroll:
    def __init__(self, font: str):
        self.font_name = font
        self._text = ""
        self._text_length = 0
        self._position_x = 0
        self._width = 0

    def set_text(self, text):
        if text != self._text:
            self._text = text
            self._text_length = FontRegistry.text_width(self.font_name, text)
            self._position_x = self._width

    def tick(self):
        self._position_x -= 1
        if self._position_x + self._text_length < 0:
            self._position_x = self._width

    def offset(self, width, height=0):
        self._width = width
        return Offset(x=self._position_x)


class Oscillate:
    def __init__(self, font: str, delay: float = 1):
        self.font_name = font
        self.delay = delay
        self._text = ""
        self._text_length = 0
        self._position_x = 0
        self._modifier = -1
        self._width = 0
        self._delay_timestamp = None

    def set_text(self, text):
        if text != self._text:
            self._text = text
            self._text_length = FontRegistry.text_width(self.font_name, text)
            self._position_x = 0
            self._modifier = -0.5

    def tick(self):
        if not self._is_delayed():
            if self._text_length >= self._width:
                self._position_x += self._modifier

                if (
                    self._modifier < 0
                    and self._position_x + self._text_length < self._width
                ):
                    self._modifier *= -1
                    self._set_delay()
                elif self._modifier > 0 and self._position_x > 0:
                    self._modifier *= -1
                    self._set_delay()

    def offset(self, width, height=0):
        self._width = width
        return Offset(x=math.floor(self._position_x))

    def _set_delay(self):
        self._delay_timestamp = time.time()

    def _is_delayed(self):
        return (
            self._delay_timestamp is not None
            and time.time() - self.delay < self._delay_timestamp
        )
