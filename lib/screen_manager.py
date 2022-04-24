import time
from threading import Event, Lock, Thread

from rgbmatrix import RGBMatrix, RGBMatrixOptions


class ScreenManager(Thread):
    def __init__(self, screen=None):
        super().__init__()
        # Configuration for the matrix
        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = "adafruit-hat-pwm"
        self.matrix = RGBMatrix(options=options)

        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.stop_run = Event()
        self.daemon = True
        self.last_render_time = None
        self.data_thread = None
        self.data = None
        self.data_lock = Lock()
        self.last_data_time = None
        self.should_render = True
        self.screen_lock = Lock()
        self.screen = screen

    def set_screen(self, screen):
        with self.screen_lock:
            self.matrix.Clear()
            self.screen = screen
            self.last_render_time = None
            self.data = None
            self.last_data_time = None
            self.should_render = True

    def stop(self):
        self.stop_run.set()

    def run(self):
        while not self.stop_run.is_set():
            with self.screen_lock:
                if self.screen is not None:
                    self.run_data()
                    self.run_render()

        self.matrix.Clear()

    def run_data(self):
        if self.screen.fetch_data_delay() is not None and not self.is_data_thread_running() and (not self.last_data_time or (time.time() - self.last_data_time) > self.screen.fetch_data_delay()):
            self.last_data_time = time.time()
            self.data_thread = Thread(target=self.run_fetch_data, daemon=True)
            self.data_thread.start()

    def is_data_thread_running(self):
        return self.data_thread is not None and self.data_thread.is_alive()

    def run_render(self):
        if self.screen.animation_delay() is not None and (not self.last_render_time or (time.time() - self.last_render_time) > self.screen.animation_delay()):
            self.should_render = True

        if self.should_render:
            self.offscreen_canvas.Clear()
            self.screen.render(self.offscreen_canvas, self.get_data())
            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

            self.last_render_time = time.time()
            self.should_render = False

    def set_data(self, data):
        with self.data_lock:
            old_data = self.data
            self.data = data
            if (data != old_data):
                self.should_render = True

    def get_data(self):
        return_data = None
        with self.data_lock:
            return_data = self.data
        return return_data

    def run_fetch_data(self):
        self.set_data(self.screen.fetch_data())
