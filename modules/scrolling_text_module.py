from rgbmatrix import graphics

from .base_module import BaseModule


class ScrollingTextModule(BaseModule):
  def __init__(self, matrix, text):
    super().__init__(matrix)
    self.text = text
    self.offscreen_canvas = self.matrix.CreateFrameCanvas()
    self.font = graphics.Font()
    self.font.LoadFont("../rpi-rgb-led-matrix/fonts/7x13.bdf")
    self.textColor = graphics.Color(255, 0, 255)
    self.pos = self.offscreen_canvas.width

  def delay_seconds(self):
    return 0.05

  def render(self):
    self.offscreen_canvas.Clear()
    len = graphics.DrawText(self.offscreen_canvas, self.font, self.pos, 10, self.textColor, self.text)
    self.pos -= 1
    if (self.pos + len < 0):
      self.pos = self.offscreen_canvas.width

    self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
