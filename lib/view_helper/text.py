import time
from dataclasses import dataclass

from rgbmatrix import graphics


@dataclass
class TextRenderData:
    text: str
    font: graphics.Font
    text_color: graphics.Color
    position_x: int
    position_y: int


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


class MultilineTextScroller:
    def __init__(self, font, text_color, positions_y, text_colors=None):
        self.font = font
        self.text_color = text_color
        self.positions_y = positions_y
        self.texts = [""] * len(positions_y)
        self.positions_x = [0] * len(positions_y)
        self.max_length = 0
        self.initialized = False
        self.text_colors = (
            text_colors if text_colors else [text_color] * len(positions_y)
        )

    def update_texts(self, texts):
        if texts != self.texts:
            self.texts = texts
            self.initialized = False

    def render(self, canvas):
        if not self.texts or all(not text for text in self.texts):
            return

        if not self.initialized:
            self.positions_x = [canvas.width] * len(self.texts)
            self.initialized = True
            self.max_length = 0

        for i, text in enumerate(self.texts):
            if not text:
                continue

            length = graphics.DrawText(
                canvas,
                self.font,
                self.positions_x[i],
                self.positions_y[i],
                self.text_colors[i],
                text,
            )
            self.max_length = max(self.max_length, length)
            self.positions_x[i] -= 1

        if all(pos + self.max_length < 0 for pos in self.positions_x):
            self.positions_x = [canvas.width] * len(self.texts)


class MultilineTextOscillator:
    def __init__(self, font, text_color, positions_y, delay=1, text_colors=None):
        self.font = font
        self.text_color = text_color
        self.positions_y = positions_y
        self.delay = delay
        self.delay_timestamp = None
        self.texts = [""] * len(positions_y)
        self.positions_x = [0] * len(positions_y)
        self.max_length = 0
        self.modifier = -1
        self.initialized = False
        self.text_colors = (
            text_colors if text_colors else [text_color] * len(positions_y)
        )

    def update_texts(self, texts):
        if texts != self.texts:
            self.texts = texts
            self.initialized = False

    def render(self, canvas):
        if not self.texts or all(not text for text in self.texts):
            return

        if not self.initialized:
            self.positions_x = [0] * len(self.texts)
            self.modifier = -1
            self.max_length = 0
            self.initialized = True

        for i, text in enumerate(self.texts):
            if not text:
                continue

            length = graphics.DrawText(
                canvas,
                self.font,
                self.positions_x[i],
                self.positions_y[i],
                self.text_colors[i],
                text,
            )
            self.max_length = max(self.max_length, length)

        if not self.is_delayed():
            if self.max_length >= canvas.width:
                self.positions_x = [
                    position + self.modifier for position in self.positions_x
                ]

            if self.modifier == 1:
                positions_offscreen = [
                    position for position in self.positions_x if position < 0
                ]
            else:
                positions_offscreen = [
                    position
                    for position in self.positions_x
                    if position + self.max_length >= canvas.width
                ]

            if not positions_offscreen:
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
