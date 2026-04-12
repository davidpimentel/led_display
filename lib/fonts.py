from rgbmatrix import graphics


class FontRegistry:
    _cache = {}

    @classmethod
    def get(cls, name):
        if name not in cls._cache:
            font = graphics.Font()
            font.LoadFont(f"./fonts/{name}.bdf")
            cls._cache[name] = font
        return cls._cache[name]

    @classmethod
    def text_width(cls, name, text):
        font = cls.get(name)
        return sum(font.CharacterWidth(c) for c in bytearray(text.encode("utf-8")))


def get_font(font_path):
    font = graphics.Font()
    font.LoadFont(font_path)
    return font


# Backward compat
FONTS = {
    "4x6": get_font("./fonts/4x6.bdf"),
    "6x9": get_font("./fonts/6x9.bdf"),
    "7x13": get_font("./fonts/7x13.bdf"),
    "5x8": get_font("./fonts/5x8.bdf"),
    "6x10": get_font("./fonts/6x10.bdf"),
    "6x12": get_font("./fonts/6x12.bdf"),
}
