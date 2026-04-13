from lib.matrix import graphics


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
