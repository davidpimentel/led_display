from rgbmatrix import graphics
from screens.base_screen import BaseScreen


class Screen(BaseScreen):
    def __init__(self):
        super().__init__()
        self.red = 255
        self.green = 0
        self.blue = 0

    def animation_delay(self):
        return 3

    def render(self, canvas, data):
      for x in range(0, canvas.width):
        for y in range(0, canvas.height):
          canvas.SetPixel(x, y, self.red, self.green, self.blue)

      temp = self.red
      self.red = self.green
      self.green = self.blue
      self.blue = temp
