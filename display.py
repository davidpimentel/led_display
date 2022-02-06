from flask import Flask, redirect, render_template, request
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from modules.gym_count_module import GymCountModule
from modules.scrolling_text_module import ScrollingTextModule
from modules.subway.g_train import GTrain
from modules.subway.l_train import LTrain
from modules.who_chooses_module import WhoChoosesModule
from modules.citibike import Citibike


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
        }
        self.module = self.modules["G Train"]()

    def run(self):
        self.module.start()
        self.flask_app.run(host="0.0.0.0")

    def route_hello_world(self):
        return render_template("index.html", modules=list(self.modules.keys()))

    def route_change_module(self):
        module_name = request.form["module_name"]
        self.module.stop()
        self.module = self.modules[module_name]()
        self.module.start()
        return redirect("/")


Display().run()
