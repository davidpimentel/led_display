import os
from dataclasses import dataclass

import requests
import spotipy
from lib.colors import COLORS
from lib.fonts import FONTS
from lib.view_helper.text import MultilineTextOscillator, TextRenderData
from PIL import Image
from rgbmatrix import graphics
from screens.base_screen import BaseScreen
from spotipy.cache_handler import CacheFileHandler
from spotipy.oauth2 import SpotifyOAuth


@dataclass
class Data:
    artist_name: str
    song_name: str
    album_image_url: str

class Screen(BaseScreen):
    def __init__(self, username=None):
        super().__init__(display_indefinitely=True)
        scope = "user-read-currently-playing"
        self.font = FONTS["4x6"]
        self.white = COLORS["white"]
        self.gray = COLORS["gray"]
        cache_path = ".cache-" + username
        cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_path)
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(open_browser=False, scope=scope, cache_handler=cache_handler))
        self.multiline_scroller = MultilineTextOscillator()

    def fetch_data_interval(self):
        return 5

    def fetch_data(self):
        currently_playing = self.sp.currently_playing()

        if currently_playing is None:
            return None

        item = currently_playing["item"]
        album_image_url = item["album"]["images"][2]["url"]
        artist_name = item["artists"][0]["name"]
        song_name = item["name"]

        return Data(
            artist_name=artist_name,
            song_name=song_name,
            album_image_url=album_image_url
        )


    def animation_interval(self):
        return 0.05

    def render(self, canvas, data):

        if data is None:
            graphics.DrawText(
                canvas, self.font, 4, 10, self.white, "NOTHING PLAYING"
            )
            return

            # im = Image.open(requests.get(album_image_url, stream=True).raw)
            # im = im.resize((32, 32), Image.NEAREST)

            # canvas.SetImage(
            #     im.convert("RGB"), offset_x=3, offset_y=3
            # )

        self.multiline_scroller.scroll_text(
            canvas,
            [
                TextRenderData(
                    font=self.font,
                    position_x=4,
                    position_y=10,
                    text_color=self.white,
                    text=data.song_name
                ),
                TextRenderData(
                    font=self.font,
                    position_x=4,
                    position_y=20,
                    text_color=self.gray,
                    text=data.artist_name
                )
            ]
        )
