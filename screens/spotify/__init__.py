import os

import requests
import spotipy
from lib.colors import COLORS
from lib.fonts import FONTS
from PIL import Image
from rgbmatrix import graphics
from screens.base_screen import BaseScreen
from spotipy.cache_handler import CacheFileHandler
from spotipy.oauth2 import SpotifyOAuth


class Screen(BaseScreen):
    def __init__(self, username=None):
        super().__init__()
        scope = "user-read-currently-playing"
        self.font = FONTS["6x9"]
        self.text_color = COLORS["white"]
        cache_path = ".cache-" + username
        cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_path)
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(open_browser=False, scope=scope, cache_handler=cache_handler))
        self.current_song_id = None

    def animation_delay(self):
        return 3

    def render(self, canvas, data):
      currently_playing = self.sp.currently_playing()

      if currently_playing is None:
        self.current_song_id = None
        graphics.DrawText(
            canvas, self.font, 4, 10, self.text_color, "NOTHING PLAYING"
        )
        return

      song_id = currently_playing["item"]["id"]
      if song_id != self.current_song_id:
        self.current_song_id = song_id
        item = currently_playing["item"]
        album_image_url = item["album"]["images"][2]["url"]
        artist_name = item["artists"][0]["name"]
        song_name = item["name"]

        # im = Image.open(requests.get(album_image_url, stream=True).raw)
        # im = im.resize((32, 32), Image.NEAREST)

        # canvas.SetImage(
        #     im.convert("RGB"), offset_x=3, offset_y=3
        # )

        graphics.DrawText(
            canvas, self.font, 4, 10, self.text_color, artist_name
        )

        graphics.DrawText(
            canvas, self.font, 4, 20, self.text_color, song_name
        )
