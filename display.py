import sentry_sdk
from dotenv import load_dotenv
from flask import (Flask, redirect, render_template, request,
                   send_from_directory)
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from screens.citibike import Citibike
from screens.clock_screen import ClockScreen
from screens.color_test import ColorTest
from screens.gym_count_screen import GymCountScreen
from screens.scrolling_text_screen import ScrollingTextScreen
from screens.spotify_screen import SpotifyScreen
from screens.subway.g_train import GTrain
from screens.subway.l_train import LTrain
from screens.who_chooses_screen import WhoChoosesScreen


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

        # Screens
        self.screens = {
            "Gym Count Screen": lambda: GymCountScreen(self.matrix),
            "Who Chooses Screen": lambda: WhoChoosesScreen(self.matrix),
            "Scrolling Text Screen": lambda: ScrollingTextScreen(
                self.matrix, "HELLO WORLD!!!"
            ),
            "G Train": lambda: GTrain(self.matrix),
            "L Train": lambda: LTrain(self.matrix),
            "Citibike": lambda: Citibike(self.matrix),
            "Clock Screen": lambda: ClockScreen(self.matrix),
            "Color Test": lambda: ColorTest(self.matrix),
            "Spotify": lambda: SpotifyScreen(self.matrix)
        }
        self.screen = self.screens["Clock Screen"]()

    def run(self):
        self.screen.start()
        self.flask_app.run(host="0.0.0.0")

    def route_hello_world(self):
        return render_template("index.html", screens=list(self.screens.keys()))

    def route_change_screen(self):
        screen_name = request.form["screen_name"]
        if self.screen:
          self.screen.stop()

        self.screen = self.screens[screen_name]()
        self.screen.start()
        return redirect("/")

    def route_turn_off_screen(self):
        if self.screen:
          self.screen.stop()
          self.screen = None

        return redirect("/")

    def route_pwa_manfiest(self):
      return send_from_directory('templates', 'manifest.json')


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
