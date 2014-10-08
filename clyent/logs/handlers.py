from __future__ import absolute_import, print_function, unicode_literals

import sys
import logging
from .colors import color
from .formatters import ColorFormatter, FormatterWrapper

class ColorStreamHandler(logging.Handler):

    def __init__(self, use_color=None, level=logging.INFO, show_tb=False):

        logging.Handler.__init__(self, level=level)

        if use_color is None:
            use_color = sys.stdout.isatty()

        self.use_color = use_color

        self.setFormatter(ColorFormatter(show_tb=show_tb))

    def emit(self, record):

        if not self.filter(record):
            return

        fmt = self.format(record)

        if record.levelno == logging.INFO:
            stream = sys.stdout
        else:
            stream = sys.stderr

        if isinstance(fmt, (list, tuple)):
            for item in fmt:
                if isinstance(item, color):
                    if self.use_color:
                        with item(stream) as text:
                            stream.write(text)
                    else:
                        stream.write(item.text)
                else:
                    stream.write(item)
                stream.write(' ')
        else:
            stream.write(fmt)

        stream.write('\n')

        if hasattr(stream, 'flush'):
            stream.flush()

def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    h = ColorStreamHandler(True, logging.DEBUG)
    logger.addHandler(h)

    logger.debug("DEBUG")
    logger.info("INFO")
    logger.warn("WARN")
    logger.error("ERROR")

    FormatterWrapper.wrap(h, prefix=color('prefix |', [color.WHITE, color.BACKGROUND_COLORS[0]]))

    logger.debug("DEBUG")
    logger.info("INFO")
    logger.warn("WARN")
    logger.error("ERROR")

if __name__ == '__main__':
    main()
