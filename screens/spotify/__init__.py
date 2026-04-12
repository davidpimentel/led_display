from dataclasses import dataclass

import spotipy
from lib.colors import Colors
from lib.ui import AnimatedText, Oscillate, Padding, Positioned, Stack, Text
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
        cache_path = ".cache-" + username
        cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_path)
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                open_browser=False, scope=scope, cache_handler=cache_handler
            )
        )
        self.song_oscillator = Oscillate(font="4x6", delay=1)
        self.artist_oscillator = Oscillate(font="4x6", delay=1)

    def setup(self):
        self.run_on_interval(self._fetch_spotify, seconds=5)
        self.run_on_interval(self._animate, seconds=0.05)

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
        self.song_oscillator.tick()
        self.artist_oscillator.tick()
        self.set_state()

    def build(self, state: SpotifyState):
        if not state.is_playing:
            return Stack(children=[
                Positioned(x=4, y=4, child=Text("NOTHING PLAYING", font="4x6", color=Colors.white))
            ])

        return Stack(children=[
            Padding(Positioned(x=0, y=4, child=AnimatedText(state.song_name, font="4x6", color=Colors.white, animator=self.song_oscillator)), left=5),
            Padding(Positioned(x=0, y=14, child=AnimatedText(state.artist_name, font="4x6", color=Colors.blue, animator=self.artist_oscillator)), left=5),
        ])
