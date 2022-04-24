import json
import subprocess
from dataclasses import dataclass
from urllib import request

from lib.colors import COLORS
from lib.fonts import FONTS
from PIL import Image
from rgbmatrix import graphics

from ..base_screen import BaseScreen


@dataclass
class Data:
    num_bikes: str
    num_ebikes: str
    station_name: str


class Screen(BaseScreen):
    def __init__(self, station_id=None, station_name=None):
        super().__init__()
        self.font = FONTS["5x8"]
        self.white = COLORS["white"]
        self.green = COLORS["green"]
        self.bike = Image.open("./images/bike.png")
        self.ebike = Image.open("./images/ebike.png")

        self.station_id = station_id
        self.station_name = station_name

    def fetch_data_interval(self):
        return 30
    def fetch_data(self):
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

        return Data(
            num_bikes=num_bikes,
            num_ebikes=num_ebikes,
            station_name=station_name
        )

    def get_color_for_range(self, count):
        if count < 100:
            return self.green

    def text_offset(self, char):
        return 61 - len(char) * 4

    def render(self, canvas, data):
        if data is not None:
            canvas.SetImage(self.bike.convert("RGB"), offset_x=3, offset_y=10)

            canvas.SetImage(
                self.ebike.convert("RGB"),
                offset_x=self.text_offset(data.num_ebikes) - 5,
                offset_y=23,
            )

            graphics.DrawText(
                canvas, self.font, 2, 7, self.white, data.station_name.upper()
            )

            graphics.DrawText(
                canvas,
                self.font,
                self.text_offset(data.num_bikes),
                18,
                self.white,
                data.num_bikes,
            )

            graphics.DrawText(
                canvas,
                self.font,
                self.text_offset(data.num_ebikes),
                28,
                self.white,
                data.num_ebikes,
            )
