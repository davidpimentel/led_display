from PIL import Image
from rgbmatrix import graphics

from .base_module import BaseModule


class ImageModule(BaseModule):
  def __init__(self, matrix, image_path):
    super().__init__(matrix)
    self.image_path = image_path

  def delay_seconds(self):
    return 100

  def render(self):
    self.matrix.Clear()
    image = Image.open(self.image_path)
    # Make image fit our screen.
    image.thumbnail((self.matrix.width, self.matrix.height), Image.NEAREST)

    self.matrix.SetImage(image.convert('RGB'))

