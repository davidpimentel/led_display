from dataclasses import dataclass, field
from typing import List

from lib.colors import Colors
from lib.ui import PixelGrid
from screens.base_screen import BaseScreen

TICK_SECONDS = 0.1

# Classic glider, offsets relative to its top-left corner:
#   . X .
#   . . X
#   X X X
GLIDER = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
BLINKER = [(1, 0), (1, 1), (1, 2)]


@dataclass
class GameOfLifeState:
    grid: List[List[int]] = field(default_factory=list)


class Screen(BaseScreen[GameOfLifeState]):
    def __init__(self, grid = None):
        self._override_grid = grid
        super().__init__(initial_state=GameOfLifeState())

    def setup(self):
        self.set_state(grid=self._override_grid or self._initial_grid())
        self.run_on_interval(self._tick, seconds=TICK_SECONDS, immediate=False)

    def _empty_grid(self):
        return [[0] * self.width for _ in range(self.height)]

    def _initial_grid(self):
        grid = self._empty_grid()
        for dx, dy in GLIDER:
            grid[dy][dx] = 1

        for dx,dy in BLINKER:
            grid[14 + dy][30 + dx] = 1

        return grid

    def _next_generation(self, grid):
        w = self.width
        h = self.height
        new = [[0] * w for _ in range(h)]
        for y in range(h):
            up = (y - 1) % h
            down = (y + 1) % h
            row = grid[y]
            row_up = grid[up]
            row_down = grid[down]
            for x in range(w):
                left = (x - 1) % w
                right = (x + 1) % w
                n = (
                    row_up[left] + row_up[x] + row_up[right]
                    + row[left] + row[right]
                    + row_down[left] + row_down[x] + row_down[right]
                )
                alive = row[x]
                if (alive and (n == 2 or n == 3)) or (not alive and n == 3):
                    new[y][x] = 1
        return new

    def _tick(self):
        state = self.get_state()
        self.set_state(grid=self._next_generation(state.grid))

    def build(self, state: GameOfLifeState):
        return PixelGrid(self.width, self.height, pixels=state.grid, color=Colors.green)
