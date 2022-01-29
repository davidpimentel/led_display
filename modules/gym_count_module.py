import json
import subprocess

from lib.colors import COLORS
from lib.fonts import FONTS
from PIL import Image
from rgbmatrix import graphics

from .base_module import BaseModule


class GymCountModule(BaseModule):
  def __init__(self, matrix):
    super().__init__(matrix)
    self.offscreen_canvas = self.matrix.CreateFrameCanvas()
    self.vital_logo = Image.open('./images/vital_logo.png')
    self.font = FONTS['6x9']
    self.white = COLORS['white']
    self.green = COLORS['green']

  def delay_seconds(self):
    return 30

  def get_color_for_range(self, count):
    if count < 100:
      return self.green

  def render(self):
    people_at_gym = str(subprocess.check_output(['curl', 'https://display.safespace.io/value/live/a7796f34']).decode('utf-8'))
    weather = json.loads(subprocess.check_output(['curl', 'api.openweathermap.org/data/2.5/weather?q=Brooklyn&appid=96d91031ccf9c0f23cabe15440f20be0&units=imperial']).decode('utf-8'))
    feels_like_temp = str(int(weather['main']['feels_like']))
    self.offscreen_canvas.Clear()

    self.offscreen_canvas.SetImage(self.vital_logo.convert('RGB'), offset_x=3, offset_y=3)

    graphics.DrawText(self.offscreen_canvas, self.font, 8, 28, self.green, people_at_gym)
    graphics.DrawText(self.offscreen_canvas, self.font, 42, 28, self.white, feels_like_temp + '°')

    self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
