from lib.matrix import graphics
from lib.colors import Color
from lib.fonts import FontRegistry
from lib.ui.widget import Size, Widget


class Text(Widget):
    def __init__(self, text: str, font: str = "5x8", color: Color = None):
        self.text = str(text)
        self.font_name = font
        self.font = FontRegistry.get(font)
        self.color = color

    def measure(self, available_width, available_height):
        width = FontRegistry.text_width(self.font_name, self.text)
        return Size(width, self.font.height)

    def paint(self, canvas, x, y, available_width, available_height):
        graphics.DrawText(canvas, self.font, x, y + self.font.baseline, self.color.graphics, self.text)


class AnimatedText(Text):
    def __init__(self, text: str, font: str = "5x8", color: Color = None, animator=None):
        super().__init__(text, font, color)
        self.animator = animator
        self.animator.set_text(text)

    def paint(self, canvas, x, y, available_width, available_height):
        offset = self.animator.offset(available_width, available_height)
        super().paint(canvas, x + offset.x, y + offset.y, available_width, available_height)


class Rect(Widget):
    def __init__(self, width: int, height: int, color: Color = None, filled: bool = True):
        self.w = width
        self.h = height
        self.color = color
        self.filled = filled

    def measure(self, available_width, available_height):
        return Size(self.w, self.h)

    def paint(self, canvas, x, y, available_width, available_height):
        gc = self.color.graphics
        if self.filled:
            for row in range(self.h):
                graphics.DrawLine(canvas, x, y + row, x + self.w - 1, y + row, gc)
        else:
            graphics.DrawLine(canvas, x, y, x + self.w - 1, y, gc)
            graphics.DrawLine(canvas, x, y + self.h - 1, x + self.w - 1, y + self.h - 1, gc)
            graphics.DrawLine(canvas, x, y, x, y + self.h - 1, gc)
            graphics.DrawLine(canvas, x + self.w - 1, y, x + self.w - 1, y + self.h - 1, gc)


class Img(Widget):
    def __init__(self, image):
        self.image = image

    def measure(self, available_width, available_height):
        if self.image is None:
            return Size(0, 0)
        return Size(self.image.width, self.image.height)

    def paint(self, canvas, x, y, available_width, available_height):
        if self.image is not None:
            canvas.SetImage(self.image, x, y)


class Line(Widget):
    def __init__(self, x1: int, y1: int, x2: int, y2: int, color: Color = None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color

    def measure(self, available_width, available_height):
        return Size(abs(self.x2 - self.x1) + 1, abs(self.y2 - self.y1) + 1)

    def paint(self, canvas, x, y, available_width, available_height):
        graphics.DrawLine(canvas, x + self.x1, y + self.y1, x + self.x2, y + self.y2, self.color.graphics)


class Spacer(Widget):
    def __init__(self, width: int = 0, height: int = 0):
        self.w = width
        self.h = height

    def measure(self, available_width, available_height):
        return Size(self.w, self.h)
