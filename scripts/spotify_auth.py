import sys

import spotipy
from dotenv import load_dotenv
from spotipy.cache_handler import CacheFileHandler
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

# hacky arg parsing
if len(sys.argv) != 3 or sys.argv[1] != "--user":
  sys.exit("you must provide --user [username]")

cache_path = ".cache-" + sys.argv[2]
scope = "user-read-currently-playing"

cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_path)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(open_browser=False, scope=scope, cache_handler=cache_handler))
print(sp.me())
