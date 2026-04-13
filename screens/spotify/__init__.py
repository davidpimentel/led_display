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
    def __init__(self, artist_name=None, song_name=None, username=None):
        self.song_oscillator = Oscillate(font="5x8", delay=5)
        self.artist_oscillator = Oscillate(font="5x8", delay=5)
        self.is_using_spotify_api = True
        
        # If we're getting a song name or artist name, let's just display it, else we use the spotify api
        if (artist_name is not None or song_name is not None):
            initial_state=SpotifyState(artist_name=artist_name.upper(), song_name=song_name.upper(), is_playing=True)
            self.is_using_spotify_api = False
            super().__init__(initial_state=initial_state, display_indefinitely=True)
            return

        super().__init__(initial_state=SpotifyState(), display_indefinitely=True)
        
        scope = "user-read-currently-playing"
        cache_path = ".cache-" + username
        cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_path)
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                open_browser=False, scope=scope, cache_handler=cache_handler
            )
        )

    def setup(self):
        if self.is_using_spotify_api:
            self.run_on_interval(self._fetch_spotify, seconds=5)

        self.run_on_interval(self._animate, seconds=0.05)

    def _fetch_spotify(self):
        currently_playing = self.sp.currently_playing()

        if currently_playing is None:
            self.set_state(is_playing=False)
            return

        item = currently_playing["item"]
        artist_name = item["artists"][0]["name"].upper()
        song_name = item["name"].upper()

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
                Positioned(x=10, y=8, child=Text("NOTHING", font="6x9", color=Colors.white)),
                Positioned(x=10, y=18, child=Text("PLAYING", font="6x9", color=Colors.white))
            ])

        return Stack(children=[
            Padding(AnimatedText(state.song_name, font="5x8", color=Colors.white, animator=self.song_oscillator), left=4, top=8),
            Padding(AnimatedText(state.artist_name, font="5x8", color=Colors.white.dimmed(0.5), animator=self.artist_oscillator), left=4, top=18),
        ])
