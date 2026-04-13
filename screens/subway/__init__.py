from dataclasses import dataclass

from lib.colors import Colors
from lib.subway_times import SubwayTimes
from lib.ui import Img, Line, Positioned, Stack, Text
from PIL import Image
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

    def build(self, state: SubwayState):
        if not state.court_sq:
            return Stack(children=[])

        return Stack(children=[
            Positioned(x=3, y=2, child=Img(self.g_train_logo)),
            Positioned(x=18, y=1, child=Text("COURT SQ", font="4x6", color=Colors.white)),
            Positioned(x=18, y=8, child=Text(state.court_sq, font="4x6", color=Colors.yellow)),
            Positioned(x=0, y=15, child=Line(0, 0, 63, 0, color=Colors.gray)),
            Positioned(x=3, y=18, child=Img(self.g_train_logo)),
            Positioned(x=18, y=18, child=Text("CHURCH AVE", font="4x6", color=Colors.white)),
            Positioned(x=18, y=25, child=Text(state.church_ave, font="4x6", color=Colors.yellow)),
        ])
