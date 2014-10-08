from clyent.logs.colors.base import BaseColor

class PosixColor(BaseColor):
    WHITE = 97
    YELLO = 93
    BLUE = 94
    GREEN = 92
    RED = 91
    BOLD = 1

    DEFAULT = 0

    UNDERLINE = 4

    BACKGROUND_COLORS = range(40, 48) + [100, 102, 104, 105, 106]

    @classmethod
    def set_colors(cls, stream, colors):
        col = list(colors)
        for c in col:
            stream.write('\033[%im' % c)

