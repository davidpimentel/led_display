import time
from threading import Event, Thread


class BaseModule(Thread):
  def __init__(self, matrix):
    super().__init__()
    self.matrix = matrix
    self.stop_run = Event()
    self.daemon = True

  def stop(self):
    self.stop_run.set()

  def run(self):
    while not self.stop_run.is_set():
      self.render()
      time.sleep(self.delay_seconds())

  def render(self):
    raise Exception('render() not implemented')

  def delay_seconds(self):
    raise Exception('delay_seconds() not implemented')
