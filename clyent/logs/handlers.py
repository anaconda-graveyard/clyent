from __future__ import absolute_import, print_function, unicode_literals

import logging
import sys

from clyent import colors


COLOR_MAP = {logging.ERROR: 'red',
             logging.WARN: 'yello',
             logging.DEBUG: 'blue'}

class ColorStreamHandler(logging.Handler):

    def __init__(self, level=logging.INFO, hide_tb=None):
        logging.Handler.__init__(self, level=level)

        self.hide_tb = hide_tb

    def emit(self, record):

        if not self.filter(record):
            return

        msg = self.format(record)

        if record.levelno <= logging.INFO:
            stream = sys.stdout
        else:
            stream = sys.stderr

        color = colors.Color(COLOR_MAP.get(record.levelno), file=stream)

        if record.exc_info and self.hide_tb and isinstance(record.exc_info[1], self.hide_tb):
            err = record.exc_info[1]
            msg = str(err)
            with color:
                print('[%s] ' % type(err).__name__, file=stream, end='')

            print(msg, file=stream)


        else:
            header = record.levelname if record.levelname != 'INFO' else ''
            if header.strip():
                with color:
                    print('[%s] ' % header, file=stream, end='')

            print(msg, file=stream)


def main():

    colors.initialize_colors()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    h = ColorStreamHandler(logging.DEBUG, hide_tb=Exception)
    logger.addHandler(h)

    logger.debug("DEBUG")
    logger.info("INFO")
    logger.warn("WARN")
    logger.error("ERROR")

#     FormatterWrapper.wrap(h, prefix=color('prefix |', [color.WHITE, color.BACKGROUND_COLORS[0]]))
    try:
        asdf
    except:
        logger.exception(None)

if __name__ == '__main__':
    main()
