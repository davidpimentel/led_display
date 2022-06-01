from lib.colors import COLORS
from lib.fonts import FONTS
from lib.subway_times import SubwayTimes
from PIL import Image
from rgbmatrix import graphics
from screens.base_screen import BaseScreen


class LTrain(BaseScreen):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()

        self.train_logo = Image.open("./images/subway_l.png").convert("RGB")
        self.train_logo.thumbnail((11, 11), Image.NEAREST)

        self.font = FONTS["5x8"]
        self.stationColor = COLORS["white"]
        self.clockColor = COLORS["yellow"]
        self.lineColor = COLORS["gray"]

    def animation_interval(self):
        return 30

    def render(self, data):
        self.offscreen_canvas.Clear()

        trip = SubwayTimes(train="L")
        arrivals = trip.arrivals_for(stop_id="L08N", direction="N")

        if len(arrivals) < 2:
            arrivals = ["No Data", "No Data"]

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
            f"{arrivals[0].minutes_away}min",
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
            f"{arrivals[1].minutes_away}min",
        )

        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
