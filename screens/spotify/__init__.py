from dataclasses import dataclass
from typing import Optional

import spotipy
from lib.colors import COLORS
from lib.fonts import FONTS
from lib.view_helper.text import TextOscillator
from rgbmatrix import graphics
from screens.base_screen import BaseScreen
from spotipy.oauth2 import SpotifyOAuth


@dataclass
class SpotifyState:
    artist_name: str = ""
    song_name: str = ""
    is_playing: bool = False


class Screen(BaseScreen[SpotifyState]):
    def __init__(self, username=None):
        super().__init__(initial_state=SpotifyState(), display_indefinitely=True)
        scope = "user-read-currently-playing"
        self.font = FONTS["4x6"]
        self.white = COLORS["white"]
        self.gray = COLORS["gray"]
        cache_path = ".cache-" + username
        cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_path)
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                open_browser=False, scope=scope, cache_handler=cache_handler
            )
        )
        self.song_scroller = TextOscillator(
            font=self.font, text_color=self.white, position_y=10, delay=1
        )
        self.artist_scroller = TextOscillator(
            font=self.font, text_color=self.gray, position_y=20, delay=1
        )

    def setup(self):
        self.create_interval(self._fetch_spotify, seconds=5)
        self.create_interval(self._animate, seconds=0.05)

    def _fetch_spotify(self):
        currently_playing = self.sp.currently_playing()

        if currently_playing is None:
            self.set_state(is_playing=False)
            return

        item = currently_playing["item"]
        artist_name = item["artists"][0]["name"]
        song_name = item["name"]

        self.set_state(
            artist_name=artist_name,
            song_name=song_name,
            is_playing=True,
        )

    def _animate(self):
        self.set_state()

    def render(self, canvas, state: SpotifyState):
        if not state.is_playing:
            graphics.DrawText(canvas, self.font, 4, 10, self.white, "NOTHING PLAYING")
            return

        self.song_scroller.update_text(state.song_name)
        self.artist_scroller.update_text(state.artist_name)

        self.song_scroller.render(canvas)
        self.artist_scroller.render(canvas)
