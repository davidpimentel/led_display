## Authentication
Before you can use this module you need to authenticate manually once.
In a venv, run `python scripts/spotify_auth.py --user [username]`


## Configuration
Ensure you have `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET` and `SPOTIPY_REDIRECT_URI` in your .env file, and that the redirect URI matches what you added in your spotify console (you can use the one from `.env.example`)