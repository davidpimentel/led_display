from lib.colors import COLORS
from lib.fonts import FONTS
from PIL import Image
from rgbmatrix import graphics

from modules.base_module import BaseModule


class GTrain(BaseModule):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.g_train_logo = Image.open("./images/subway_g.png").convert("RGB")
        self.g_train_logo.thumbnail((11, 11), Image.NEAREST)
        self.font = FONTS["6x9"]
        self.textColor = COLORS["white"]

    def delay_seconds(self):
        return 30

    def render(self):
        self.offscreen_canvas.Clear()

        self.offscreen_canvas.SetImage(self.g_train_logo, offset_x=1, offset_y=1)
        graphics.DrawLine(self.offscreen_canvas, 0, 15, 63, 15, self.textColor)
        self.offscreen_canvas.SetImage(self.g_train_logo, offset_x=1, offset_y=17)

        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
