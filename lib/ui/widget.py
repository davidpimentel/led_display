from dataclasses import dataclass


@dataclass
class Size:
    width: int = 0
    height: int = 0


class Widget:
    def measure(self, available_width, available_height):
        return Size(0, 0)

    def paint(self, canvas, x, y, available_width, available_height):
        pass
