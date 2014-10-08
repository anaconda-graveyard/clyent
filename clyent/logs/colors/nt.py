from contextlib import contextmanager

import win32console
from pywintypes import error as Win32Error

std_output_hdl = win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE)

if std_output_hdl is not None:
    try:
        std_output_hdl.GetConsoleScreenBufferInfo()
    except Win32Error:  # Not a valid ConsoleScreenBuffer
        std_output_hdl = None

class NTColor(object):
    YELLO = 14
    BLUE = 11
    GREEN = 10
    RED = 12
    BOLD = 0
    WHITE = 15

    DEFAULT = 15

    BACKGROUND_COLORS = [c << 4 for c in range(1, 10)]

    def __init__(self, text, colors):
        self.text = text
        self.colors = colors

    @contextmanager
    def __call__(self, stream):
        c = reduce(lambda a, b: a | b, self.colors)
        if std_output_hdl is not None:
            std_output_hdl.SetConsoleTextAttribute(c)
        try:
            yield self.text
        finally:
            if std_output_hdl is not None:
                std_output_hdl.SetConsoleTextAttribute(self.DEFAULT)

