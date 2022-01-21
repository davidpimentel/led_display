#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options = options)

offscreen_canvas = matrix.CreateFrameCanvas()
# font = graphics.Font()
# font.LoadFont("../rpi-rgb-led-matrix/fonts/7x13.bdf")
# textColor = graphics.Color(255, 255, 0)

# offscreen_canvas.Clear()
# len = graphics.DrawText(offscreen_canvas, font, 10, 10, textColor, 'testing')
# matrix.SwapOnVSync(offscreen_canvas)

matrix.SetPixel(16, 16, 255, 0, 255)
time.sleep(1)
matrix.SetPixel(16, 16, 0, 0, 255)
# offscreen_canvas.SetPixel(16, 16, 255, 0, 255)
# matrix.SwapOnVSync(offscreen_canvas)

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)