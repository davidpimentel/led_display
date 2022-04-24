from rgbmatrix import graphics


class TextScroller:
    def __init__(self):
        self.current_text = None
        self.position_x = 0
        self.position_y = 0

    def scroll_text(self, canvas, font, start_position_x, start_position_y, text_color, text):
        if text != self.current_text:
            self.current_text = text
            self.position_x = start_position_x
            self.position_y = start_position_y

        length = graphics.DrawText(
            canvas, font, self.position_x, self.position_y, text_color, text
        )
        self.position_x -= 1
        if self.position_x + length < 0:
            self.position_x = canvas.width


def right_align_text(canvas=None, text=None, font=None, font_color=None, y=0, padding=0):
    width = 0
    for character in bytearray(text.encode('utf-8')):
        width += font.CharacterWidth(character)

    width += padding
    x = canvas.width - width

    graphics.DrawText(
                canvas, font, x, y, font_color, text
            )
