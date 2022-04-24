import time
from threading import Event, Lock, Thread

from rgbmatrix import RGBMatrix, RGBMatrixOptions


class ScreenManager(Thread):
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
        self.initial_screen_render_time = None
        self.screen_complete = False
        self.screen = None

    def __reset(self):
        self.matrix.Clear()
        self.last_render_time = None
        self.data = None
        self.last_data_time = None
        self.should_render = True
        self.screen_complete = False

    def set_screen(self, screen):
        with self.screen_lock:
            self.screen = screen
            self.__reset()
            self.initial_screen_render_time = time.time()


    def stop(self):
        self.stop_run.set()

    def run(self):
        while not self.stop_run.is_set():
            with self.screen_lock:
                if self.screen is not None:
                    self.__run_data()
                    self.__run_render()
                    self.__check_screen_completed()

            if self.screen_complete:
                self.on_screen_completed() # call outside of screen lock

        self.matrix.Clear()

    def __check_screen_completed(self):
        if self.initial_screen_render_time is not None and self.screen is not None:
            if self.screen.display_duration() is not None and time.time() - self.initial_screen_render_time > self.screen.display_duration():
                self.screen_complete = True


    def __run_data(self):
        if self.screen.fetch_data_interval() is not None and not self.__is_data_thread_running() and (not self.last_data_time or (time.time() - self.last_data_time) > self.screen.fetch_data_interval()):
            self.last_data_time = time.time()
            self.data_thread = Thread(target=self.__run_fetch_data, daemon=True)
            self.data_thread.start()

    def __is_data_thread_running(self):
        return self.data_thread is not None and self.data_thread.is_alive()

    def __run_render(self):
        if self.screen.animation_interval() is not None and (not self.last_render_time or (time.time() - self.last_render_time) > self.screen.animation_interval()):
            self.should_render = True

        if self.should_render:
            self.offscreen_canvas.Clear()
            self.screen.render(self.offscreen_canvas, self.__get_data())
            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

            self.last_render_time = time.time()
            self.should_render = False

    def __set_data(self, data):
        with self.data_lock:
            old_data = self.data
            self.data = data
            if (data != old_data):
                self.should_render = True

    def __get_data(self):
        return_data = None
        with self.data_lock:
            return_data = self.data
        return return_data

    def __run_fetch_data(self):
        self.__set_data(self.screen.fetch_data())
