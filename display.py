import importlib

import sentry_sdk
import yaml
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, send_from_directory

# from rgbmatrix import RGBMatrix, RGBMatrixOptions


class Display:
    def __init__(self):
        # Configuration for the matrix
        # options = RGBMatrixOptions()
        # options.rows = 32
        # options.cols = 64
        # options.chain_length = 1
        # options.parallel = 1
        # options.hardware_mapping = "adafruit-hat-pwm"
        # self.matrix = RGBMatrix(options=options)

        # Flask app
        self.flask_app = Flask(__name__)
        self.flask_app.route("/")(self.route_hello_world)
        self.flask_app.route("/change_screen", methods=["POST"])(
            self.route_change_screen
        )

        self.flask_app.route("/turn_off_screen", methods=["POST"])(
            self.route_turn_off_screen
        )
        self.flask_app.route("/manifest.json")(self.route_pwa_manfiest)

        # Config/ Screen loading
        with open("config.yml", "r") as config_file:
            config = yaml.safe_load(config_file)

        self.screens = config["screens"]

        # pick the first screen in the dict to start
        # self.load_screen(next(iter(self.screens)))

    def run(self):
        # self.screen.start()
        self.flask_app.run(host="0.0.0.0", port="3000")

    def route_hello_world(self):
        return render_template("index.html", screens=self.screens)

    def route_change_screen(self):
        screen_name = request.form["screen_name"]
        if self.screen:
            self.screen.stop()

        self.load_screen(screen_name)
        self.screen.start()
        return redirect("/")

    def route_turn_off_screen(self):
        if self.screen:
            self.screen.stop()
            self.screen = None

        return redirect("/")

    def route_pwa_manfiest(self):
        return send_from_directory("templates", "manifest.json")

    def load_screen(self, screen_name):
        screen_dict = self.screens[screen_name]
        kwargs = screen_dict.get("args", {})
        self.screen = importlib.import_module("screens." + screen_name).Screen(
            self.matrix, **kwargs
        )


sentry_sdk.init(
    "https://4f39f9d71b4743bcbd3c04c5b1628799@o1136978.ingest.sentry.io/6189103",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)

# This loads in environment variables from .env file
load_dotenv()

Display().run()
