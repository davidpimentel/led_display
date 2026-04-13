import time
from threading import Event, Thread

from lib.ui import render_to_canvas


class ScreenThread(Thread):
    def __init__(self, matrix=None, screen=None, on_screen_completed=None):
        super().__init__()
        self.matrix = matrix
        self.screen = screen
        self.on_screen_completed = on_screen_completed

        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.stop_run = Event()
        self.daemon = True
        self.initial_screen_render_time = time.time()
        self.screen_complete = False

    def stop(self):
        self.stop_run.set()

    def run(self):
        if self.screen is not None:
            self.screen.setup()

        while not self.stop_run.is_set():
            if self.screen is not None:
                self.__run_render()
                self.__check_screen_completed()

            if self.screen_complete:
                break

            time.sleep(0.001)

        if self.screen is not None:
            self.screen.cleanup()

        self.matrix.Clear()

        if self.screen_complete and self.on_screen_completed:
            Thread(target=self.on_screen_completed, daemon=True).start()

    def __check_screen_completed(self):
        if self.initial_screen_render_time is not None and self.screen is not None:
            if (
                self.screen.display_duration() is not None
                and time.time() - self.initial_screen_render_time
                > self.screen.display_duration()
            ):
                self.screen_complete = True

    def __run_render(self):
        if self.screen._render_requested:
            self.screen._render_requested = False
            state = self.screen.get_state()
            self.offscreen_canvas.Clear()
            widget = self.screen.build(state)
            if widget is not None:
                render_to_canvas(self.offscreen_canvas, widget)
            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
