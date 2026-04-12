try:
    from rgbmatrix import graphics
except ImportError:
    from RGBMatrixEmulator import graphics

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self._graphics_color = graphics.Color(r, g, b)

    def dimmed(self, factor):
        return Color(int(self.r * factor), int(self.g * factor), int(self.b * factor))

    @property
    def graphics(self):
        return self._graphics_color


class Colors:
    white = Color(255, 255, 255)
    gray = Color(128, 128, 128)
    green = Color(134, 216, 80)
    teal = Color(89, 216, 215)
    yellow = Color(244, 193, 21)
    red = Color(255, 0, 0)
    blue = Color(0, 0, 255)


# Backward compat
COLORS = {
    "white": Colors.white.graphics,
    "gray": Colors.gray.graphics,
    "green": Colors.green.graphics,
    "teal": Colors.teal.graphics,
    "yellow": Colors.yellow.graphics,
}
