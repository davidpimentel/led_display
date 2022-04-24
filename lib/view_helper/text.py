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
    def __init__(self):
        self.text_render_data = None
        self.position_x = 0

    def scroll_text(self, canvas, text_render_data):
        if self.text_render_data is None or text_render_data != self.text_render_data:
            self.text_render_data = text_render_data
            self.position_x = self.text_render_data.position_x

        length = graphics.DrawText(
            canvas,
            text_render_data.font,
            self.position_x,
            text_render_data.position_y,
            text_render_data.text_color,
            text_render_data.text
        )
        self.position_x -= 1
        if self.position_x + length < 0:
            self.position_x = canvas.width

class MultilineTextScroller:
    def __init__(self):
        self.text_render_data_list = []
        self.positions_x = []
        self.max_length = 0

    def scroll_text(self, canvas, text_render_data_list):
        if self.text_render_data_list is None or text_render_data_list != self.text_render_data_list:
            self.text_render_data_list = text_render_data_list
            self.positions_x = [text_render_data.position_x for text_render_data in self.text_render_data_list]
            self.max_length = 0

        for i, text_render_data in enumerate(text_render_data_list):
            length = graphics.DrawText(
                canvas,
                text_render_data.font,
                self.positions_x[i],
                text_render_data.position_y,
                text_render_data.text_color,
                text_render_data.text
            )
            self.max_length = max(self.max_length, length)
            self.positions_x[i] -= 1
            if self.positions_x[i] + self.max_length < 0:
                self.positions_x = [canvas.width for pos in self.positions_x]


class MultilineTextOscillator:
    def __init__(self, delay=1):
        self.delay = delay
        self.delay_timestamp = None
        self.text_render_data_list = []
        self.positions_x = []
        self.max_length = 0
        self.modifier = -1

    def scroll_text(self, canvas, text_render_data_list):
        if self.text_render_data_list is None or text_render_data_list != self.text_render_data_list:
            self.text_render_data_list = text_render_data_list
            self.positions_x = [text_render_data.position_x for text_render_data in self.text_render_data_list]
            self.modifier = -1
            self.max_length = 0

        for i, text_render_data in enumerate(text_render_data_list):
            length = graphics.DrawText(
                canvas,
                text_render_data.font,
                self.positions_x[i],
                text_render_data.position_y,
                text_render_data.text_color,
                text_render_data.text
            )

            self.max_length = max(self.max_length, length)

        if not self.is_delayed():
            if self.max_length >= canvas.width:
                self.positions_x = [position + self.modifier for position in self.positions_x]

            if self.modifier == 1:
                positions_offscreen = [position for position in self.positions_x if position < 0]
            else:
                positions_offscreen = [position for position in self.positions_x if position + self.max_length >= canvas.width]

            if not positions_offscreen:
                self.modifier *= -1
                self.set_delay()

    def set_delay(self):
        self.delay_timestamp = time.time()

    def is_delayed(self):
        return self.delay_timestamp is not None and time.time() - self.delay < self.delay_timestamp

def right_align_text(canvas=None, text=None, font=None, font_color=None, y=0, padding=0):
    width = 0
    for character in bytearray(text.encode('utf-8')):
        width += font.CharacterWidth(character)

    width += padding
    x = canvas.width - width

    graphics.DrawText(
                canvas, font, x, y, font_color, text
            )
