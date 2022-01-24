import random

from PIL import Image
from rgbmatrix import graphics

from .base_module import BaseModule


class WhoChoosesModule(BaseModule):
  def __init__(self, matrix):
    super().__init__(matrix)
    self.rand_int = random.randint(0, 1)
    self.font = graphics.Font()
    self.font.LoadFont("./fonts/5x8.bdf")
    self.font_height = self.font.height
    self.white = graphics.Color(255, 255, 255)
    self.green = graphics.Color(134, 216, 80)
    self.teal = graphics.Color(89, 216, 215)

  def delay_seconds(self):
    return 100

  def render(self):
    self.matrix.Clear()
    images = [(Image.open('images/dave.png'), 'DAVE', self.green), (Image.open('images/nicole.png'), 'NICOLE', self.teal)]

    image, name, name_color = images[self.rand_int]

    graphics.DrawText(self.matrix, self.font, 0, self.font_height, self.white, 'YOU')
    len = graphics.DrawText(self.matrix, self.font, 0, (self.font_height * 2), self.white, 'CHOOSE:')
    graphics.DrawText(self.matrix, self.font, 0, (self.font_height * 3), name_color, name)
    self.matrix.SetImage(image.convert('RGB'), len + 1, 0)

