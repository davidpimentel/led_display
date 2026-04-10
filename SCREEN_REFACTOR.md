# StatefulScreen: React-inspired State Management for LED Screens

## Context

The current screen API splits state awkwardly: "data" comes from `fetch_data()` managed by ScreenThread, while animation state (scroll positions, counters) lives on `self` and mutates inside `render()`. There's no single mechanism for a screen to say "something changed, re-render me." This change introduces a `StatefulScreen` base class with `set_state()` / typed state / `create_interval()`, giving screen authors one clear pattern: update state, get a re-render. We migrate the weather screen as a proof of concept while keeping all existing screens working unchanged.

## Files to Change

| File | Action |
|------|--------|
| `screens/stateful_screen.py` | **CREATE** — new base class |
| `lib/screen_thread.py` | **MODIFY** — 4 small additions for lifecycle + render flag |
| `screens/weather/__init__.py` | **REWRITE** — POC migration |

## Step 1: Create `screens/stateful_screen.py`

New `StatefulScreen(BaseScreen, Generic[S])` class where `S` is a dataclass type:

- **`__init__(self, initial_state: S, **kwargs)`** — stores state, creates Lock, Event, sets `_render_requested = True` for initial render. `**kwargs` forwards `display_indefinitely`/`duration` to BaseScreen.
- **`setup(self)`** — override to register intervals. Called by ScreenThread on start.
- **`cleanup(self)`** — sets `_stop_event`, stopping all interval threads. Called by ScreenThread on stop.
- **`set_state(self, **kwargs)`** — under `_state_lock`: merges via `dataclasses.replace(self._state, **kwargs)`, sets `_render_requested = True`. With no kwargs, just triggers a re-render (for animation ticks).
- **`get_state(self) -> S`** — returns `copy.copy(self._state)` under lock.
- **`create_interval(self, fn, seconds, immediate=True)`** — spawns a daemon thread that calls `fn` every `seconds`. Uses `Event.wait(timeout=seconds)` instead of `time.sleep` for responsive shutdown. Supports async functions via `asyncio.run()`. No overlapping calls (next sleep starts after fn returns).
- **`render(self, canvas, data)`** — bridge method called by ScreenThread. Ignores `data`, calls `self._render(canvas, self.get_state())`.
- **`_render(self, canvas, state: S)`** — subclasses override this. Receives a snapshot copy of state.
- **BaseScreen overrides**: `fetch_data()`, `fetch_data_interval()`, `animation_interval()` all return `None` so ScreenThread's old timer logic is inert.

## Step 2: Modify `lib/screen_thread.py`

Four backward-compatible additions (all guarded by `hasattr`):

1. **setup hook** — at start of `run()`, before while loop: `if hasattr(self.screen, 'setup'): self.screen.setup()`
2. **`_render_requested` check** — at top of `__run_render()`: if `screen._render_requested` is True, set `should_render = True` and clear the flag
3. **cleanup hook** — after while loop exits, before `matrix.Clear()`: `if hasattr(self.screen, 'cleanup'): self.screen.cleanup()`
4. **Busy-loop mitigation** — add `time.sleep(0.001)` at end of while loop body (benefits all screens)

## Step 3: Migrate Weather Screen

Rewrite `screens/weather/__init__.py`:

- Define `WeatherState` dataclass with `temp`, `feels_like_temp`, `description`, `icon_image` fields (all with defaults)
- `class Screen(StatefulScreen[WeatherState])`
- `setup()`: `create_interval(self._fetch_weather, 60)` + `create_interval(self._animate, 0.04)`
- `_fetch_weather()`: same logic as current `fetch_data()`, ends with `self.set_state(temp=..., ...)`
- `_animate()`: calls `self.set_state()` with no args to trigger re-render for TextScroller
- `_render(canvas, state)`: same drawing code, reads from `state` param. Returns early if `state.icon_image is None` (no data yet)
- TextScroller stays on `self` as a stateful helper (not in state dataclass)

## Threading Model

- `set_state` is thread-safe (Lock-protected). Multiple interval threads can call it concurrently.
- `_render_requested` flag: set by `set_state` (any thread), read/cleared by ScreenThread loop. Worst-case race: one render delayed by ~1ms (one loop iteration). Imperceptible.
- `get_state` returns a shallow copy. PIL Images are shared by reference (safe because they're replaced, not mutated).
- `create_interval` threads stop via `Event.wait()` — cleanup interrupts sleep immediately.
- Screen switching: `ScreenThread.stop()` → loop exits → `cleanup()` → `_stop_event.set()` → all intervals exit.

## Step 4: Cleanup — Full Cutover (after all screens are migrated)

Once every screen extends `StatefulScreen` instead of `BaseScreen`, we can remove the dual-paradigm scaffolding and simplify the system.

### 4a: Collapse `BaseScreen` into `StatefulScreen`

- **Delete `screens/base_screen.py`**
- **Rename `StatefulScreen` → `Screen`** (or `BaseScreen` — whichever reads better) in `screens/stateful_screen.py`. Rename file to `screens/base_screen.py` to keep the canonical import path.
- Remove the `Generic[S]` parent from the base class name is optional — it can stay for typed screens, or we can keep it as-is since it's just a type hint.
- Remove the bridge overrides that exist solely for backward compatibility:
  - `fetch_data()` returning `None`
  - `fetch_data_interval()` returning `None`
  - `animation_interval()` returning `None`
  - `render(self, canvas, data)` bridge that delegates to `_render`
- **Rename `_render` → `render`** — the public method screens override becomes `render(self, canvas, state: S)` directly (no more `data` parameter, no bridge).
- Remove `display_indefinitely` and `duration` from `__init__` if all screens now manage duration through other means, OR keep them if they're still useful.

### 4b: Simplify `ScreenThread`

Once all screens are StatefulScreen-based, ScreenThread no longer needs its own data-fetching or animation-interval machinery:

- **Remove `__run_data()`** entirely — screens manage their own data fetching via `create_interval`.
- **Remove `data`, `data_lock`, `data_thread`, `last_data_time`** instance variables — no longer used.
- **Remove `__set_data()`, `__get_data()`, `__run_fetch_data()`, `__is_data_thread_running()`** — all obsolete.
- **Simplify `__run_render()`** — remove the `animation_interval()` check branch. The only render trigger is `_render_requested`. The method becomes:
  ```
  if screen._render_requested:
      screen._render_requested = False
      offscreen_canvas.Clear()
      screen.render(offscreen_canvas)  # no data param
      offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
  ```
- **Remove `hasattr` guards** — `setup()` and `cleanup()` are always present (defined on the base class).
- **Remove the `if self.screen is not None` guard** if ScreenThread always has a screen.
- The `run()` method becomes:
  ```
  screen.setup()
  while not stop_run.is_set():
      if screen._render_requested:
          render and swap
      check_screen_completed()
      time.sleep(0.001)
  screen.cleanup()
  matrix.Clear()
  ```

### 4c: Update `ScreenManager.build_screen()`

- `build_screen()` currently passes `display_indefinitely` and `duration` as kwargs. Verify these still flow through correctly after the BaseScreen removal, or adjust the signature.
- No other changes needed — `importlib.import_module` pattern stays the same.

### 4d: Update all screen imports

- Every screen changes `from screens.base_screen import BaseScreen` → the new import path (e.g., `from screens.base_screen import Screen` if we kept the filename).
- Every screen's `render(self, canvas, data)` → `render(self, canvas, state: MyState)`.

### Result

After cleanup, the system has:
- **One base class** (`Screen` or `BaseScreen`) with `setup`, `cleanup`, `set_state`, `create_interval`, `render(canvas, state)`
- **One simple ScreenThread** that only does: call setup, loop checking `_render_requested` + duration, call cleanup
- **No dual-paradigm code** — no `hasattr` checks, no bridge methods, no unused data-fetching infrastructure

## Verification

1. Run the display with weather screen selected — should show weather data with scrolling text
2. Switch to a different (old-style) screen — weather intervals should stop cleanly
3. Switch back to weather — fresh setup, data fetches again
4. Verify other old-style screens still work identically
5. Check CPU usage — the 1ms sleep should reduce idle CPU vs. current busy-loop
6. (After full cutover) Run every screen, verify all work with the simplified ScreenThread
