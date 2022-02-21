from lib.colors import COLORS
from lib.fonts import FONTS
from lib.view_helper.text import TextScroller
from rgbmatrix import graphics
from screens.base_screen import BaseScreen


class Screen(BaseScreen):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.text = "HELLO WORLD"
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.font = FONTS["7x13"]
        self.text_color = COLORS["white"]
        self.text_scroller = TextScroller(self.text, self.offscreen_canvas.width, 10, self.font, self.text_color)

    def delay_seconds(self):
        return 0.05

    def render(self):
        self.offscreen_canvas.Clear()
        self.text_scroller.scroll_text(self.offscreen_canvas)
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
