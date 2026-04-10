import copy
from dataclasses import replace
from threading import Event, Lock, Thread
from typing import Generic, TypeVar

from screens.base_screen import BaseScreen

S = TypeVar("S")


class StatefulScreen(BaseScreen, Generic[S]):
    def __init__(self, initial_state: S, **kwargs):
        super().__init__(**kwargs)
        self._state = initial_state
        self._state_lock = Lock()
        self._render_requested = True
        self._stop_event = Event()
        self._intervals: list[Thread] = []

    # --- Lifecycle ---

    def setup(self):
        pass

    def cleanup(self):
        self._stop_event.set()

    # --- State management ---

    def set_state(self, **kwargs):
        with self._state_lock:
            if kwargs:
                self._state = replace(self._state, **kwargs)
            self._render_requested = True

    def get_state(self) -> S:
        with self._state_lock:
            return copy.copy(self._state)

    # --- Intervals ---

    def create_interval(self, fn, seconds: float, immediate: bool = True):
        def _loop():
            first = True
            while not self._stop_event.is_set():
                if first and not immediate:
                    first = False
                else:
                    try:
                        fn()
                    except Exception:
                        pass
                    first = False
                if self._stop_event.wait(timeout=seconds):
                    break

        thread = Thread(target=_loop, daemon=True)
        self._intervals.append(thread)
        thread.start()
        return thread

    # --- Bridge to ScreenThread ---

    def fetch_data(self):
        return None

    def fetch_data_interval(self):
        return None

    def animation_interval(self):
        return None

    def render(self, canvas, data):
        self._render(canvas, self.get_state())

    def _render(self, canvas, state: S):
        raise NotImplementedError("Subclasses must implement _render()")
