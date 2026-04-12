from lib.ui.widget import Size, Widget


class Stack(Widget):
    def __init__(self, children=None):
        self.children = children or []

    def measure(self, available_width, available_height):
        max_w = 0
        max_h = 0
        has_non_positioned = False
        for child in self.children:
            if isinstance(child, Positioned):
                continue
            has_non_positioned = True
            size = child.measure(available_width, available_height)
            max_w = max(max_w, size.width)
            max_h = max(max_h, size.height)
        if not has_non_positioned:
            return Size(available_width, available_height)
        return Size(max_w, max_h)

    def paint(self, canvas, x, y, available_width, available_height):
        for child in self.children:
            child.paint(canvas, x, y, available_width, available_height)


class Positioned(Widget):
    def __init__(self, child, x: int = 0, y: int = 0):
        self.child = child
        self.x = x
        self.y = y

    def measure(self, available_width, available_height):
        size = self.child.measure(available_width - self.x, available_height - self.y)
        return Size(self.x + size.width, self.y + size.height)

    def paint(self, canvas, x, y, available_width, available_height):
        self.child.paint(
            canvas,
            x + self.x,
            y + self.y,
            available_width - self.x,
            available_height - self.y,
        )


class Padding(Widget):
    def __init__(self, child, left: int = 0, top: int = 0, right: int = 0, bottom: int = 0):
        self.child = child
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def measure(self, available_width, available_height):
        size = self.child.measure(
            available_width - self.left - self.right,
            available_height - self.top - self.bottom,
        )
        return Size(
            size.width + self.left + self.right,
            size.height + self.top + self.bottom,
        )

    def paint(self, canvas, x, y, available_width, available_height):
        self.child.paint(
            canvas,
            x + self.left,
            y + self.top,
            available_width - self.left - self.right,
            available_height - self.top - self.bottom,
        )
