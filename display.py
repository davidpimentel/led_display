import time

from flask import Flask, redirect, render_template, request
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

from modules.gym_count_module import GymCountModule
from modules.image_module import ImageModule
from modules.scrolling_text_module import ScrollingTextModule


class Display:
  def __init__(self):
  # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'
    self.matrix = RGBMatrix(options = options)

    # Flask app
    self.flask_app = Flask(__name__)
    self.flask_app.route('/')(self.route_hello_world)
    self.flask_app.route('/change_module', methods=['POST'])(self.route_change_module)

    # Modules
    self.modules = {
      'Gym Count Module': lambda: GymCountModule(self.matrix),
      'Image Module': lambda: ImageModule(self.matrix, 'images/citi_bike.png'),
      'Scrolling Text Module': lambda: ScrollingTextModule(self.matrix, 'HELLO WORLD!!!')
    }
    self.module = self.modules['Gym Count Module']()

  def run(self):
    self.module.start()
    # self.flask_app.run(host='0.0.0.0')

  def route_hello_world(self):
      return render_template('index.html', modules=list(self.modules.keys()))

  def route_change_module(self):
    module_name = request.form['module_name']
    self.module.stop()
    self.module = self.modules[module_name]()
    self.module.start()
    return redirect("/")

Display().run()



