import importlib
import os

import sentry_sdk
import yaml
from dotenv import load_dotenv

from flask_app import FlaskApp
from lib.mqtt.adafruit_mqtt_client import AdafruitMQTTClient
from lib.scheduler import Scheduler
from lib.screen_manager import ScreenManager


class Display:
    def __init__(self):
        # Config
        with open("config.yml", "r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)

        # Screen
        self.screen_manager = ScreenManager()
        self.screen = None
        self.screens = config["screens"]
        self.load_screen(self.screens[0]["id"]) # pick the first screen in the dict to start

        # Pub/Sub
        if os.getenv("ENABLE_ADAFRUIT_MQTT") == "true":
            self.adafruit_mqtt_client = AdafruitMQTTClient(on_change_screen=self.change_screen)

        # Scheduler
        self.scheduler = None
        if config.get("schedule"):
            self.scheduler = Scheduler(config["schedule"], on_change_screen=self.change_screen)

        # Web app
        self.flask_app = FlaskApp(
            screens=self.screens,
            on_change_screen=self.change_screen,
            on_turn_off_screen=self.turn_off_screen
        )

    def run(self):
        if os.getenv("ENABLE_ADAFRUIT_MQTT") == "true":
            self.adafruit_mqtt_client.start()

        self.screen_manager.start()

        if self.scheduler:
            self.scheduler.start()

        self.flask_app.start()

    def change_screen(self, screen_id):
        self.load_screen(screen_id)

    def turn_off_screen(self):
        self.screen.set_screen(None)
        self.screen = None

    def load_screen(self, screen_id):
        screen_dict = next((screen for screen in self.screens if screen["id"] == screen_id))
        screen_name = screen_dict["screen_name"]
        kwargs = screen_dict.get("args", {})
        self.screen = importlib.import_module("screens." + screen_name).Screen(**kwargs)
        self.screen_manager.set_screen(self.screen)


sentry_sdk.init( # pylint: disable=abstract-class-instantiated
    "https://4f39f9d71b4743bcbd3c04c5b1628799@o1136978.ingest.sentry.io/6189103",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)

# This loads in environment variables from .env file
load_dotenv()

Display().run()
