import json
import subprocess

from lib.colors import COLORS
from lib.fonts import FONTS
from PIL import Image
from RGBMatrixEmulator import graphics
from urllib import request

from ..base_module import BaseModule


class Citibike(BaseModule):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.font = FONTS["4x6"]
        self.white = COLORS["white"]
        self.green = COLORS["green"]
        self.bike = Image.open("./images/bike.png")
        self.ebike = Image.open("./images/ebike.png")

    def delay_seconds(self):
        return 30

    def get_color_for_range(self, count):
        if count < 100:
            return self.green

    def text_offset(self, char):
        return 61 - len(char) * 4

    def render(self):
        station_id = "432"  # A and 7th
        # station_id = "3101"  # bedford
        # station_id = "3108"  # Nassau

        station_name = None
        # station_name = "Bedford Ave"

        response = request.urlopen(
            "https://gbfs.citibikenyc.com/gbfs/es/station_status.json"
        )

        list = json.loads(response.read())["data"]["stations"]

        station_status = next(
            (status for status in list if status["station_id"] == station_id), None
        )

        num_bikes = str(station_status["num_bikes_available"])
        num_ebikes = str(station_status["num_ebikes_available"])

        if not station_name:
            response = request.urlopen(
                "https://gbfs.citibikenyc.com/gbfs/es/station_information.json"
            )

            list = json.loads(response.read())["data"]["stations"]

            station_info = next(
                (status for status in list if status["station_id"] == station_id), None
            )

            station_name = station_info["name"].replace("Avenue", "Ave")

        self.offscreen_canvas.Clear()

        self.offscreen_canvas.SetImage(self.bike.convert("RGB"), offset_x=6, offset_y=9)

        self.offscreen_canvas.SetImage(
            self.ebike.convert("RGB"),
            offset_x=self.text_offset(num_ebikes) - 5,
            offset_y=23,
        )

        graphics.DrawText(
            self.offscreen_canvas, self.font, 2, 7, self.white, station_name.upper()
        )

        graphics.DrawText(
            self.offscreen_canvas,
            self.font,
            self.text_offset(num_bikes),
            18,
            self.white,
            num_bikes,
        )

        graphics.DrawText(
            self.offscreen_canvas,
            self.font,
            self.text_offset(num_ebikes),
            28,
            self.white,
            num_ebikes,
        )

        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
