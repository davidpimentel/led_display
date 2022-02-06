import json

from flask import Flask, redirect, render_template, request
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from modules.gym_count_module import GymCountModule
from modules.scrolling_text_module import ScrollingTextModule
from modules.subway.g_train import GTrain
from modules.subway.l_train import LTrain
from modules.who_chooses_module import WhoChoosesModule
from modules.citibike import Citibike

# Modules
module_spec = {
    "Gym Count": lambda matrix, options: GymCountModule(matrix, **options),
    "Who Chooses": lambda matrix, options: WhoChoosesModule(matrix, **options),
    "Scrolling Text": lambda matrix, options: ScrollingTextModule(matrix, **options),
    "G Train": lambda matrix, options: GTrain(matrix, **options),
    "L Train": lambda matrix, options: LTrain(matrix, **options),
    "Citibike": lambda matrix, options: Citibike(matrix, **options),
}


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

        config = json.load(open("config.json"))

        modules = {}

        for mod_config in config["modules"]:

            def init(mod_config):
                def func():
                    return module_spec[mod_config["module"]](
                        self.matrix, mod_config["options"]
                    )

                return func

            modules[mod_config["label"]] = init(mod_config)

        self.modules = modules
        self.module = self.modules[config["default"]]()

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
