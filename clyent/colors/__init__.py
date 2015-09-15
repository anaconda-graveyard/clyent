from __future__ import print_function
import sys
from contextlib import contextmanager

from clyent.colors.color import Color
from clyent.colors.color_formatter import print_colors


def initialize_colors(when='tty'):

    assert when in ['tty', 'always', 'never'], when

    if when == 'never':
        return

    if sys.stdout.isatty() or when == 'always':
        sys.stdout = ColorStream(sys.stdout)

    if sys.stderr.isatty() or when == 'always':
        sys.stderr = ColorStream(sys.stderr)


class ColorStream(object):

    def __init__(self, stream):
        self.stream = stream
        self.current_color_id = None

    def write(self, data):
        n = self.stream.write(data)
        return n

    def flush(self):
        self.stream.flush()


    def set_color(self, color_id):

        last_color_id = self.current_color_id

        self.stream.write('\033[%sm' % (color_id or 0))

        self.current_color_id = color_id
        return last_color_id


def test():
    initialize_colors()
    print("test")

    with Color('red'):
        print("This is red")
        print_colors('hello {=blue!c:blue}')
        print("This is red again")

    for color in range(256):
        with Color(color):
            print(color)


if __name__ == '__main__':
    test()
