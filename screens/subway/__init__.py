from lib.colors import COLORS
from lib.fonts import FONTS
from lib.subway_times import SubwayTimes
from PIL import Image
from rgbmatrix import graphics
from screens.base_screen import BaseScreen


class Screen(BaseScreen):
    def __init__(self):
        super().__init__()
        self.g_train_logo = Image.open("./images/subway_g.png").convert("RGB")
        self.g_train_logo.thumbnail((11, 11), Image.NEAREST)

        self.font = FONTS["4x6"]
        self.stationColor = COLORS["white"]
        self.clockColor = COLORS["yellow"]
        self.lineColor = COLORS["grey"]

    def animation_interval(self):
        return 30

    def render(self, canvas, data):
        trip = SubwayTimes(train="G")

        # NOTE: This gets all upcoming arrivals to the given station (Nassau in this case).
        # If you want to implement filtering based on a threshold of minutes you can do it here.
        court_sq_arrivals = trip.arrivals_for(stop_id="G28N", direction="N")
        church_ave_arrivals = trip.arrivals_for(stop_id="G28S", direction="S")

        if len(court_sq_arrivals) < 1:
            court_sq = "No Trains"
        else:
            court_sq = f"{court_sq_arrivals[0].minutes_away}min"

        if len(church_ave_arrivals) < 1:
            church_ave = "No Trains"
        else:
            church_ave = f"{church_ave_arrivals[0].minutes_away}min"

        canvas.SetImage(self.g_train_logo, offset_x=3, offset_y=2)
        graphics.DrawText(
            canvas, self.font, 18, 7, self.stationColor, "COURT SQ"
        )
        graphics.DrawText(
            canvas,
            self.font,
            18,
            14,
            self.clockColor,
            court_sq,
        )

        graphics.DrawLine(canvas, 0, 15, 63, 15, self.lineColor)

        canvas.SetImage(self.g_train_logo, offset_x=3, offset_y=18)
        graphics.DrawText(
            canvas, self.font, 18, 24, self.stationColor, "CHURCH AVE"
        )
        graphics.DrawText(
            canvas,
            self.font,
            18,
            31,
            self.clockColor,
            church_ave,
        )
