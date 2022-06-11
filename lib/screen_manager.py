from rgbmatrix import RGBMatrix, RGBMatrixOptions

from lib.screen_thread import ScreenThread


class ScreenManager:
    def __init__(self, on_screen_completed):
        super().__init__()
        self.on_screen_completed = on_screen_completed

        # Configuration for the matrix
        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = "adafruit-hat-pwm"
        self.matrix = RGBMatrix(options=options)
        self.screen_thread = None

    def set_screen(self, screen):
        if self.screen_thread is not None:
            self.screen_thread.stop()

        self.screen_thread = ScreenThread(
            matrix=self.matrix,
            screen=screen,
            on_screen_completed=self.on_screen_completed
        )
        self.screen_thread.start()

