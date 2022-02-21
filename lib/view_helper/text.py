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

