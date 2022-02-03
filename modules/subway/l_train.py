from lib.colors import COLORS
from lib.fonts import FONTS
from PIL import Image
from rgbmatrix import graphics

from modules.base_module import BaseModule

from lib import subway_times


class LTrain(BaseModule):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()

        self.train_logo = Image.open("./images/subway_l.png").convert("RGB")
        self.train_logo.thumbnail((11, 11), Image.NEAREST)

        self.font = FONTS["5x8"]
        self.stationColor = COLORS["white"]
        self.clockColor = COLORS["yellow"]
        self.lineColor = COLORS["grey"]

    def delay_seconds(self):
        return 30

    def render(self):
        self.offscreen_canvas.Clear()

        arrivals = subway_times.SubwayTimes().upcoming_arrivals()

        self.offscreen_canvas.SetImage(self.train_logo, offset_x=3, offset_y=2)
        graphics.DrawText(
            self.offscreen_canvas, self.font, 18, 7, self.stationColor, "8TH AVE"
        )
        graphics.DrawText(
            self.offscreen_canvas,
            self.font,
            18,
            14,
            self.clockColor,
            f"{arrivals[0]}min",
        )

        graphics.DrawLine(self.offscreen_canvas, 0, 15, 63, 15, self.lineColor)

        self.offscreen_canvas.SetImage(self.train_logo, offset_x=3, offset_y=18)
        graphics.DrawText(
            self.offscreen_canvas, self.font, 18, 24, self.stationColor, "8TH AVE"
        )
        graphics.DrawText(
            self.offscreen_canvas,
            self.font,
            18,
            31,
            self.clockColor,
            f"{arrivals[1]}min",
        )

        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
