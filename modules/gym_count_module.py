import subprocess

from rgbmatrix import graphics

from .base_module import BaseModule


class GymCountModule(BaseModule):
  def __init__(self, matrix):
    super().__init__(matrix)
    self.offscreen_canvas = self.matrix.CreateFrameCanvas()
    self.font = graphics.Font()
    self.font.LoadFont("../rpi-rgb-led-matrix/fonts/4x6.bdf")
    self.textColor = graphics.Color(255, 0, 255)
    self.pos = self.offscreen_canvas.width

  def delay_seconds(self):
    return 30

  def render(self):
    capacity = subprocess.check_output(['curl', 'https://display.safespace.io/value/live/a7796f34']).decode('utf-8')
    self.offscreen_canvas.Clear()
    len = graphics.DrawText(self.offscreen_canvas, self.font, 10, 10, self.textColor, "Gym Capacity:")
    graphics.DrawText(self.offscreen_canvas, self.font, 10, 20, self.textColor, str(capacity))

    self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
