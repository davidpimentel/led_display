import yaml
from dotenv import load_dotenv

from flask_app import FlaskApp
from lib.screen_manager import ScreenManager


class Display:
    def __init__(self):
        # Config
        with open("config.yml", "r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)

        # Screen
        self.screen_manager = ScreenManager(on_screen_completed=self.set_to_default)
        self.screen = None
        self.screen_id = None
        self.screens = config["screens"]
        self.set_to_default()

        # Web app
        self.flask_app = FlaskApp(
            screens=self.screens,
            on_change_screen=self.change_screen,
            on_turn_off_screen=self.turn_off_screen,
            on_default_screen=self.set_to_default,
            get_current_screen=self.get_current_screen,
        )

    def run(self):
        self.flask_app.start()

    def set_to_default(self):
        self.load_screen(self.screens[0]["id"], {}, display_indefinitely=True)

    def override_screen(self, screen_id, kwargs):
        self.load_screen(screen_id, kwargs, display_indefinitely=True)

    def change_screen(self, screen_id, kwargs, display_indefinitely, duration):
        self.load_screen(screen_id, kwargs, display_indefinitely, duration)

    def turn_off_screen(self):
        self.screen.set_screen(None)
        self.screen = None
        self.screen_id = None

    def load_screen(self, screen_id, kwargs, display_indefinitely=False, duration=None):
        screen_dict = next(
            (screen for screen in self.screens if screen["id"] == screen_id)
        )
        screen_name = screen_dict["screen_name"]
        merged_kwargs = {**(screen_dict.get("args", {})), **kwargs}
        self.screen = ScreenManager.build_screen(
            screen_name, merged_kwargs, display_indefinitely, duration
        )
        self.screen_id = screen_id

        self.screen_manager.set_screen(self.screen)

    def get_current_screen(self):
        return self.screen_id


# This loads in environment variables from .env file
load_dotenv()

Display().run()
