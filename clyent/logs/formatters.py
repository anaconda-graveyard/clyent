from __future__ import print_function, absolute_import
import logging
from .colors import color
import traceback
from clyent.errors import ClyentError

class FormatterWrapper(object):

    def __init__(self, formatter, prefix='', suffix=''):
        self.prefix = prefix
        self.suffix = suffix
        self.formatter = formatter

    def format(self, record):
        result = self.formatter.format(record)
        if not isinstance(result, list):
            result = [result]

        if self.prefix:
            result.insert(0, self.prefix)
        if self.suffix:
            result.append(self.suffix)
        return result

    @classmethod
    def wrap(cls, handler, prefix='', suffix=''):
        old_formatter = handler.formatter or logging.Formatter()
        new_formatter = cls(old_formatter, prefix, suffix)
        handler.setFormatter(new_formatter)


class ColorFormatter(object):

    COLOR_MAP = {'ERROR': (color.BOLD, color.RED),
                 'WARNING': (color.BOLD, color.YELLO),
                 'DEBUG': (color.BOLD, color.BLUE),
                 }

    def color_map(self, header, level):
        header = '[%s]' % header
        if level in self.COLOR_MAP:
            return color(header, self.COLOR_MAP[level])
        else:
            return header

    def __init__(self, show_tb=False):

        if show_tb is False:
            show_tb = (ClyentError, KeyboardInterrupt)
        elif show_tb is True:
            show_tb = ()

        self.show_tb = show_tb

    def format(self, record):
        if record.levelno == logging.INFO:
            header = None
            message = record.getMessage()
        else:
            if record.exc_info:
                err = record.exc_info[1]
                header = type(err).__name__
                result = [self.color_map(header, record.levelname)]
                if getattr(err, 'message', None):
                    result.append(str(err.message))
                elif err.args:
                    result.append(str(err.args[0]))

                if self.show_tb is True or not isinstance(err, self.show_tb):
                    message = ''.join(traceback.format_exception(*record.exc_info))
                    result.append('\n' + message)
                return result

            else:
                header = record.levelname.lower()
                message = record.getMessage()

        if header:
            header = self.color_map(header, record.levelname)
            return [header, '%s' % message]
        else:
            return message
