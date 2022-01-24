import subprocess

from PIL import Image
from rgbmatrix import graphics

from .base_module import BaseModule


class SubwayModule(BaseModule):
  def __init__(self, matrix):
    super().__init__(matrix)
    self.offscreen_canvas = self.matrix.CreateFrameCanvas()
    self.g_train_logo = Image.open('./images/G.png').convert('RGB')
    self.g_train_logo.thumbnail((11, 11), Image.NEAREST)
    self.font = graphics.Font()
    self.font.LoadFont("./fonts/6x9.bdf")
    self.textColor = graphics.Color(255, 255, 255)

  def delay_seconds(self):
    return 30

  def render(self):
    self.offscreen_canvas.Clear()

    self.offscreen_canvas.SetImage(self.g_train_logo, offset_x=1, offset_y=1)
    graphics.DrawLine(self.offscreen_canvas, 0, 15, 63, 15, self.textColor)
    self.offscreen_canvas.SetImage(self.g_train_logo, offset_x=1, offset_y=17)

    self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
