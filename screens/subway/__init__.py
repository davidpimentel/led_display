from dataclasses import dataclass

from lib.colors import COLORS
from lib.fonts import FONTS
from lib.subway_times import SubwayTimes
from PIL import Image
from rgbmatrix import graphics
from screens.base_screen import BaseScreen


@dataclass
class SubwayState:
    court_sq: str = ""
    church_ave: str = ""


class Screen(BaseScreen[SubwayState]):
    def __init__(self):
        super().__init__(initial_state=SubwayState())
        self.g_train_logo = Image.open("./images/subway_g.png").convert("RGB")
        self.g_train_logo.thumbnail((11, 11), Image.NEAREST)

        self.font = FONTS["4x6"]
        self.stationColor = COLORS["white"]
        self.clockColor = COLORS["yellow"]
        self.lineColor = COLORS["gray"]

    def setup(self):
        self.run_on_interval(self._fetch_subway, seconds=30)

    def _fetch_subway(self):
        trip = SubwayTimes(train="G")

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

        self.set_state(court_sq=court_sq, church_ave=church_ave)

    def render(self, canvas, state: SubwayState):
        if not state.court_sq:
            return

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
            state.court_sq,
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
            state.church_ave,
        )
