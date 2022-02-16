import sentry_sdk
from flask import Flask, redirect, render_template, request
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from modules.citibike import Citibike
from modules.clock_module import ClockModule
from modules.color_test import ColorTest
from modules.gym_count_module import GymCountModule
from modules.scrolling_text_module import ScrollingTextModule
from modules.subway.g_train import GTrain
from modules.subway.l_train import LTrain
from modules.who_chooses_module import WhoChoosesModule


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
        self.flask_app.route("/change_module", methods=["POST"])(
            self.route_change_module
        )

        self.flask_app.route("/turn_off_screen", methods=["POST"])(
            self.route_turn_off_screen
        )

        # Modules
        self.modules = {
            "Gym Count Module": lambda: GymCountModule(self.matrix),
            "Who Chooses Module": lambda: WhoChoosesModule(self.matrix),
            "Scrolling Text Module": lambda: ScrollingTextModule(
                self.matrix, "HELLO WORLD!!!"
            ),
            "G Train": lambda: GTrain(self.matrix),
            "L Train": lambda: LTrain(self.matrix),
            "Citibike": lambda: Citibike(self.matrix),
            "Clock Module": lambda: ClockModule(self.matrix),
            "Color Test": lambda: ColorTest(self.matrix)
        }
        self.module = self.modules["Clock Module"]()

    def run(self):
        self.module.start()
        self.flask_app.run(host="0.0.0.0")

    def route_hello_world(self):
        return render_template("index.html", modules=list(self.modules.keys()))

    def route_change_module(self):
        module_name = request.form["module_name"]
        if self.module:
          self.module.stop()

        self.module = self.modules[module_name]()
        self.module.start()
        return redirect("/")

    def route_turn_off_screen(self):
        if self.module:
          self.module.stop()
          self.module = None

        return redirect("/")


sentry_sdk.init(
    "https://4f39f9d71b4743bcbd3c04c5b1628799@o1136978.ingest.sentry.io/6189103",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)

Display().run()
