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

    def stop(self):
        self.stop_run.set()

    def run(self):
        while not self.stop_run.is_set():
            self.run_data()
            self.run_render()

        self.matrix.Clear()

    def run_data(self):
        if self.fetch_data_delay_seconds() is not None and not self.is_data_thread_running() and (not self.last_data_time or (time.time() - self.last_data_time) > self.fetch_data_delay_seconds()):
            self.last_data_time = time.time()
            self.data_thread = Thread(target=self.fetch_data, daemon=True)
            self.data_thread.start()

    def is_data_thread_running(self):
        return self.data_thread is not None and self.data_thread.is_alive()

    def run_render(self):
        if not self.last_render_time or (time.time() - self.last_render_time) > self.delay_seconds():
              self.render()
              self.last_render_time = time.time()

    def set_data(self, data):
        with self.data_lock:
            self.data = data

    def get_data(self):
        return_data = None
        with self.data_lock:
            return_data = self.data
        return return_data


    # Methods to override in subclass

    def fetch_data(self):
        pass
        print("fetch data")

    def fetch_data_delay_seconds(self):
        return None

    def render(self):
        raise Exception("render() not implemented")

    def delay_seconds(self):
        raise Exception("delay_seconds() not implemented")
