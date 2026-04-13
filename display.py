import argparse

import yaml
from dotenv import load_dotenv

from flask_app import FlaskApp
from lib.screen_discovery import discover_screens
from lib.screen_manager import ScreenManager


class Display:
    def __init__(self, initial_screen=None):
        # Config
        try:
            with open("config.yml", "r", encoding="utf-8") as config_file:
                config = yaml.safe_load(config_file) or {}
        except FileNotFoundError:
            config = {}

        # Screen
        self.screen_manager = ScreenManager(on_screen_completed=self.set_to_default)
        self.screen = None
        self.screen_id = None
        self.screen_names = discover_screens()
        self.screen_args = config.get("screen_args", {})
        self.default_screen = config.get("default_screen", "clock")
        if initial_screen:
            self.load_screen(initial_screen, {}, display_indefinitely=True)
        else:
            self.set_to_default()

        # Web app
        self.flask_app = FlaskApp(
            screens=self.screen_names,
            on_change_screen=self.change_screen,
            on_turn_off_screen=self.turn_off_screen,
            on_default_screen=self.set_to_default,
            get_current_screen=self.get_current_screen,
        )

    def run(self):
        self.flask_app.start()

    def set_to_default(self):
        self.load_screen(self.default_screen, {}, display_indefinitely=True)

    def override_screen(self, screen_id, kwargs):
        self.load_screen(screen_id, kwargs, display_indefinitely=True)

    def change_screen(self, screen_id, kwargs, display_indefinitely, duration):
        self.load_screen(screen_id, kwargs, display_indefinitely, duration)

    def turn_off_screen(self):
        self.screen.set_screen(None)
        self.screen = None
        self.screen_id = None

    def load_screen(self, screen_name, kwargs, display_indefinitely=False, duration=None):
        config_args = self.screen_args.get(screen_name, {})
        merged_kwargs = {**config_args, **kwargs}
        self.screen = ScreenManager.build_screen(
            screen_name, merged_kwargs, display_indefinitely, duration
        )
        self.screen_id = screen_name

        self.screen_manager.set_screen(self.screen)

    def get_current_screen(self):
        return self.screen_id


# This loads in environment variables from .env file
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--initial-screen", default=None)
args = parser.parse_args()

Display(initial_screen=args.initial_screen).run()
