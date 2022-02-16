import time
from threading import Event, Thread


class BaseModule(Thread):
    def __init__(self, matrix):
        super().__init__()
        self.matrix = matrix
        self.stop_run = Event()
        self.daemon = True
        self.last_render_time = None

    def stop(self):
        self.stop_run.set()

    def run(self):
        while not self.stop_run.is_set():
            if not self.last_render_time or (time.time() - self.last_render_time) > self.delay_seconds():
              self.render()
              self.last_render_time = time.time()

        self.matrix.Clear()

    def render(self):
        raise Exception("render() not implemented")

    def delay_seconds(self):
        raise Exception("delay_seconds() not implemented")
