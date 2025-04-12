import time
from dataclasses import dataclass

from rgbmatrix import graphics


class TextScroller:
    def __init__(self, font, text_color, position_y):
        self.font = font
        self.text_color = text_color
        self.position_y = position_y
        self.text = ""
        self.position_x = 0
        self.initialized = False

    def update_text(self, text):
        if text != self.text:
            self.text = text
            self.initialized = False

    def render(self, canvas):
        if not self.text:
            return

        if not self.initialized:
            self.position_x = canvas.width
            self.initialized = True

        length = graphics.DrawText(
            canvas,
            self.font,
            self.position_x,
            self.position_y,
            self.text_color,
            self.text,
        )
        self.position_x -= 1
        if self.position_x + length < 0:
            self.position_x = canvas.width


class TextOscillator:
    def __init__(self, font, text_color, position_y, delay=1):
        self.font = font
        self.text_color = text_color
        self.position_y = position_y
        self.delay = delay
        self.delay_timestamp = None
        self.text = ""
        self.position_x = 0
        self.text_length = 0
        self.modifier = -1
        self.initialized = False

    def update_text(self, text):
        if text != self.text:
            self.text = text
            self.initialized = False

    def render(self, canvas):
        if not self.text:
            return

        if not self.initialized:
            self.position_x = 0
            self.modifier = -1
            self.text_length = 0
            self.initialized = True

        length = graphics.DrawText(
            canvas,
            self.font,
            self.position_x,
            self.position_y,
            self.text_color,
            self.text,
        )
        self.text_length = length

        if not self.is_delayed():
            if self.text_length >= canvas.width:
                self.position_x += self.modifier

                if self.modifier == 1 and self.position_x < 0:
                    self.modifier *= -1
                    self.set_delay()
                elif (
                    self.modifier == -1
                    and self.position_x + self.text_length >= canvas.width
                ):
                    self.modifier *= -1
                    self.set_delay()

    def set_delay(self):
        self.delay_timestamp = time.time()

    def is_delayed(self):
        return (
            self.delay_timestamp is not None
            and time.time() - self.delay < self.delay_timestamp
        )


def right_align_text(
    canvas=None, text=None, font=None, font_color=None, y=0, padding=0
):
    width = 0
    for character in bytearray(text.encode("utf-8")):
        width += font.CharacterWidth(character)

    width += padding
    x = canvas.width - width

    graphics.DrawText(canvas, font, x, y, font_color, text)
