from rgbmatrix import graphics


def get_font(font_path):
  font = graphics.Font()
  font.LoadFont(font_path)
  return font

FONTS = {
  '6x9': get_font('./fonts/6x9.bdf'),
  '7x13': get_font('./fonts/7x13.bdf'),
  '5x8': get_font('./fonts/5x8.bdf')
}
