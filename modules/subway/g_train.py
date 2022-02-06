from lib.colors import COLORS
from lib.fonts import FONTS
from PIL import Image
from rgbmatrix import graphics

from modules.base_module import BaseModule
from lib.subway_times import SubwayTimes


class GTrain(BaseModule):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.g_train_logo = Image.open("./images/subway_g.png").convert("RGB")
        self.g_train_logo.thumbnail((11, 11), Image.NEAREST)

        self.font = FONTS["4x6"]
        self.stationColor = COLORS["white"]
        self.clockColor = COLORS["yellow"]
        self.lineColor = COLORS["grey"]

    def delay_seconds(self):
        return 30

    def render(self):
        self.offscreen_canvas.Clear()

        trip = SubwayTimes(train="G")

        # NOTE: This gets all upcoming arrivals to the given station (Nassau in this case).
        # If you want to implement filtering based on a threshold of minutes you can do it here.
        court_sq_arrivals = trip.arrivals_for(stop_id="G28N", direction="N")
        church_ave_arrivals = trip.arrivals_for(stop_id="G28S", direction="S")

        if len(court_sq_arrivals) < 1:
            court_sq = ["No Trains"]
        else:
            court_sq = court_sq_arrivals[0].minutes_away

        if len(church_ave_arrivals) < 1:
            church_ave = ["No Trains"]
        else:
            church_ave = church_ave_arrivals[0].minutes_away

        self.offscreen_canvas.SetImage(self.g_train_logo, offset_x=3, offset_y=2)
        graphics.DrawText(
            self.offscreen_canvas, self.font, 18, 7, self.stationColor, "COURT SQ"
        )
        graphics.DrawText(
            self.offscreen_canvas,
            self.font,
            18,
            14,
            self.clockColor,
            f"{court_sq}min",
        )

        graphics.DrawLine(self.offscreen_canvas, 0, 15, 63, 15, self.lineColor)

        self.offscreen_canvas.SetImage(self.g_train_logo, offset_x=3, offset_y=18)
        graphics.DrawText(
            self.offscreen_canvas, self.font, 18, 24, self.stationColor, "CHURCH AVE"
        )
        graphics.DrawText(
            self.offscreen_canvas,
            self.font,
            18,
            31,
            self.clockColor,
            f"{church_ave}min",
        )

        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
