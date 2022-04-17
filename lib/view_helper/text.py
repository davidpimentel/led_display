from rgbmatrix import graphics


class TextScroller:
    def __init__(self, text, start_position_x, start_position_y, font, text_color):
        self.text = text
        self.position_x = start_position_x
        self.position_y = start_position_y
        self.font = font
        self.text_color = text_color

    def scroll_text(self, canvas):
        len = graphics.DrawText(
            canvas, self.font, self.position_x, self.position_y, self.text_color, self.text
        )
        self.position_x -= 1
        if self.position_x + len < 0:
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
