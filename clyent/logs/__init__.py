from __future__ import print_function, absolute_import, unicode_literals

import logging
from logging.handlers import RotatingFileHandler
from os import makedirs
from os.path import join, exists, dirname
import sys

from clyent import errors
from clyent.colors import initialize_colors

from .handlers import ColorStreamHandler, JsonFormatter


def log_unhandled_exception(logger):
    def excepthook(*exc_info):
        logger.error('', exc_info=exc_info)
        sys.exit(1)

    return excepthook

def setup_logging(logger, level, use_color=None, logfile=None, show_tb=False, as_json=False):
    initialize_colors()

    logger.setLevel(logging.DEBUG)

    cli_logger = logging.getLogger('cli-logger')
    cli_logger.setLevel(logging.ERROR)
    if as_json:
        fmt = JsonFormatter()
    else:
        fmt = logging.Formatter("[%(asctime)s] %(message)s")

    if logfile:
        if not exists(dirname(logfile)): makedirs(dirname(logfile))
        hndlr = RotatingFileHandler(logfile, maxBytes=10 * (1024 ** 2), backupCount=5,)
        hndlr.setLevel(logging.ERROR)
        hndlr.setFormatter(fmt)

        logger.addHandler(hndlr)

        cli_logger.addHandler(hndlr)

    exceptions = (errors.ClyentError, KeyboardInterrupt)
    if not as_json:
        shndlr = ColorStreamHandler(show_tb=show_tb, exceptions=exceptions)
    else:
        shndlr = logging.StreamHandler(stream=sys.stdout)
        shndlr.setFormatter(fmt)
    shndlr.setLevel(level)
    logger.addHandler(shndlr)

    sys.excepthook = log_unhandled_exception(logger)

