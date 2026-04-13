import json
from dataclasses import dataclass
from urllib import request

from lib.colors import Colors
from lib.ui import Img, Positioned, Stack, Text
from PIL import Image
from screens.base_screen import BaseScreen


@dataclass
class CitibikeState:
    num_bikes: str = ""
    num_ebikes: str = ""
    station_name: str = ""


class Screen(BaseScreen[CitibikeState]):
    def __init__(self, station_id=None, station_name=None):
        super().__init__(initial_state=CitibikeState())
        self.bike = Image.open("./images/bike.png").convert("RGB")
        self.ebike = Image.open("./images/ebike.png").convert("RGB")
        self.station_id = station_id
        self.station_name = station_name

    def setup(self):
        self.run_on_interval(self._fetch_data, seconds=30)

    def _fetch_data(self):
        response = request.urlopen(
            "https://gbfs.citibikenyc.com/gbfs/es/station_status.json"
        )

        stations = json.loads(response.read())["data"]["stations"]

        station_status = next(
            (status for status in stations if status["station_id"] == self.station_id), None
        )

        num_bikes = str(station_status["num_bikes_available"])
        num_ebikes = str(station_status["num_ebikes_available"])

        if not self.station_name:
            response = request.urlopen(
                "https://gbfs.citibikenyc.com/gbfs/es/station_information.json"
            )

            stations = json.loads(response.read())["data"]["stations"]

            station_info = next(
                (status for status in stations if status["station_id"] == self.station_id), None
            )

            station_name = station_info["name"].replace("Avenue", "Ave")
        else:
            station_name = self.station_name

        self.set_state(
            num_bikes=num_bikes,
            num_ebikes=num_ebikes,
            station_name=station_name,
        )

    def _text_offset(self, char):
        return 61 - len(char) * 4

    def build(self, state: CitibikeState):
        if not state.num_bikes:
            return Stack(children=[])

        return Stack(children=[
            Positioned(x=2, y=0, child=Text(state.station_name.upper(), font="5x8", color=Colors.white)),
            Positioned(x=3, y=10, child=Img(self.bike)),
            Positioned(x=self._text_offset(state.num_bikes), y=10, child=Text(state.num_bikes, font="5x8", color=Colors.white)),
            Positioned(x=self._text_offset(state.num_ebikes) - 5, y=23, child=Img(self.ebike)),
            Positioned(x=self._text_offset(state.num_ebikes), y=20, child=Text(state.num_ebikes, font="5x8", color=Colors.white)),
        ])
