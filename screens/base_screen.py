import time
from threading import Event, Lock, Thread


class BaseScreen(Thread):
    def __init__(self, matrix):
        super().__init__()
        self.matrix = matrix
        self.stop_run = Event()
        self.daemon = True
        self.last_render_time = None
        self.data_thread = Thread()
        self.data = None
        self.data_lock = Lock()
        self.last_data_time = None
        self.should_render = True

    def stop(self):
        self.stop_run.set()

    def run(self):
        while not self.stop_run.is_set():
            self.run_data()
            self.run_render()

        self.matrix.Clear()

    def run_data(self):
        if self.fetch_data_delay() is not None and not self.is_data_thread_running() and (not self.last_data_time or (time.time() - self.last_data_time) > self.fetch_data_delay()):
            self.last_data_time = time.time()
            self.data_thread = Thread(target=self.run_fetch_data, daemon=True)
            self.data_thread.start()

    def is_data_thread_running(self):
        return self.data_thread is not None and self.data_thread.is_alive()

    def run_render(self):
        if self.animation_delay() is not None and (not self.last_render_time or (time.time() - self.last_render_time) > self.animation_delay()):
            self.should_render = True

        if self.should_render:
            self.render(self.get_data())
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
        self.set_data(self.fetch_data())


    # Methods to override in subclass

    def fetch_data(self):
        pass

    def fetch_data_delay(self):
        return None

    def render(self, data):
        raise Exception("render() not implemented")

    def animation_delay(self):
        return None
