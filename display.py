import importlib
import os

import sentry_sdk
import yaml
from dotenv import load_dotenv
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from flask_app import FlaskApp
from lib.mqtt.adafruit_mqtt_client import AdafruitMQTTClient
from scheduler import Scheduler


class Display:
    def __init__(self):
        # Configuration for the matrix
        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = "adafruit-hat-pwm"
        self.matrix = RGBMatrix(options=options)

        # Config/ Screen loading
        with open("config.yml", "r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)

        self.screen = None
        self.screens = config["screens"]

        # pick the first screen in the dict to start
        self.load_screen(next(iter(self.screens)))

        if os.getenv("ENABLE_ADAFRUIT_MQTT") == "true":
            self.adafruit_mqtt_client = AdafruitMQTTClient(on_change_screen=self.change_screen)

        self.scheduler = Scheduler(on_change_screen=self.change_screen)
        self.flask_app = FlaskApp(
            screens=self.screens,
            on_change_screen=self.change_screen,
            on_turn_off_screen=self.turn_off_screen
        )

    def run(self):
        if os.getenv("ENABLE_ADAFRUIT_MQTT") == "true":
            self.adafruit_mqtt_client.start()
        self.screen.start()
        # self.scheduler.start()
        self.flask_app.start()

    def change_screen(self, screen_name):
        if self.screen:
            self.screen.stop()

        self.load_screen(screen_name)
        self.screen.start()

    def turn_off_screen(self):
        if self.screen:
            self.screen.stop()
            self.screen = None

    def load_screen(self, screen_name):
        screen_dict = self.screens[screen_name]
        kwargs = screen_dict.get("args", {})
        self.screen = importlib.import_module("screens." + screen_name).Screen(
            self.matrix, **kwargs
        )


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
