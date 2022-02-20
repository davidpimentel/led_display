from rgbmatrix import graphics

from screens.base_screen import BaseScreen


class Screen(BaseScreen):
    def __init__(self, matrix):
        super().__init__(matrix)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.red = 255
        self.green = 0
        self.blue = 0

    def delay_seconds(self):
        return 3

    def render(self):
      for x in range(0, self.offscreen_canvas.width):
        for y in range(0, self.offscreen_canvas.height):
          self.offscreen_canvas.SetPixel(x, y, self.red, self.green, self.blue)

      temp = self.red
      self.red = self.green
      self.green = self.blue
      self.blue = temp

      self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
