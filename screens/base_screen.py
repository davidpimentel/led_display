import copy
from dataclasses import replace
from threading import Event, Lock, Thread
from typing import Generic, TypeVar

S = TypeVar("S")


class BaseScreen(Generic[S]):
    def __init__(self, initial_state: S, display_indefinitely=False, duration=30):
        self.display_indefinitely = display_indefinitely
        self.duration = duration
        self._state = initial_state
        self._state_lock = Lock()
        self._render_requested = True
        self._stop_event = Event()

    def setup(self):
        pass

    def cleanup(self):
        self._stop_event.set()

    def set_state(self, **kwargs):
        with self._state_lock:
            if kwargs:
                self._state = replace(self._state, **kwargs)
            self._render_requested = True

    def get_state(self) -> S:
        with self._state_lock:
            return copy.copy(self._state)

    def create_interval(self, fn, seconds: float, immediate: bool = True):
        def _loop():
            if not immediate:
                self._stop_event.wait(timeout=seconds)
            while not self._stop_event.is_set():
                try:
                    fn()
                except Exception:
                    pass
                self._stop_event.wait(timeout=seconds)

        Thread(target=_loop, daemon=True).start()

    def display_duration(self):
        return None if self.display_indefinitely else self.duration

    def render(self, canvas, state: S):
        raise NotImplementedError("Subclasses must implement render()")
