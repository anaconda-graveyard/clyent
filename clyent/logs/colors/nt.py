from clyent.logs.colors.base import BaseColor
from pywintypes import error as Win32Error
import win32console


std_output_hdl = win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE)

if std_output_hdl is not None:
    try:
        std_output_hdl.GetConsoleScreenBufferInfo()
    except Win32Error:  # Not a valid ConsoleScreenBuffer
        std_output_hdl = None

class NTColor(BaseColor):
    YELLO = 14
    BLUE = 11
    GREEN = 10
    RED = 12
    BOLD = 0
    WHITE = 15

    DEFAULT = 15

    BACKGROUND_COLORS = [c << 4 for c in range(1, 10)]

    @classmethod
    def set_colors(cls, stream, colors):
        c = reduce(lambda a, b: a | b, colors)
        if std_output_hdl is not None:
            std_output_hdl.SetConsoleTextAttribute(c)

