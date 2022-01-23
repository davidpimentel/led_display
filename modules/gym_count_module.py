import subprocess

from PIL import Image
from rgbmatrix import graphics

from .base_module import BaseModule


class GymCountModule(BaseModule):
  def __init__(self, matrix):
    super().__init__(matrix)
    self.offscreen_canvas = self.matrix.CreateFrameCanvas()
    self.vital_logo = Image.open('./images/vital_logo.png')
    self.vital_logo.thumbnail((32, 15), Image.NEAREST)
    self.drop = Image.open('./images/drop.png')
    self.drop.thumbnail((10, 16), Image.NEAREST)
    self.font = graphics.Font()
    self.font.LoadFont("./fonts/6x9.bdf")
    self.textColor = graphics.Color(255, 255, 255)
    self.pos = self.offscreen_canvas.width



  def delay_seconds(self):
    return 30

  def render(self):
    capacity = subprocess.check_output(['curl', 'https://display.safespace.io/value/live/a7796f34']).decode('utf-8')
    self.offscreen_canvas.Clear()

    self.offscreen_canvas.SetImage(self.vital_logo.convert('RGB'), offset_x=5, offset_y=2)
    self.offscreen_canvas.SetImage(self.drop.convert('RGB'), offset_x=16, offset_y=16)

    len = graphics.DrawText(self.offscreen_canvas, self.font, 42, 10, self.textColor, str(capacity))
    graphics.DrawLine(self.offscreen_canvas, 41, 15, 61, 15, self.textColor)
    len = graphics.DrawText(self.offscreen_canvas, self.font, 42, 27, self.textColor, '76°')

    self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
