from __future__ import absolute_import, print_function, unicode_literals

import imp
import logging
import os
from os.path import dirname
import pkgutil

from clyent.errors import ShowHelp
from clyent.logs.colors import color
from clyent.logs.colors.printer import print_colors
import sys


def add_default_arguments(parser, version=None):

    parser.add_argument('--show-traceback', action='store_true', default=not sys.stdout.isatty(),
                        help='Show the full traceback for chalmers user errors (default: %(default)s)')
    parser.add_argument('--hide-traceback', action='store_false', dest='show_traceback',
                        help='Hide the full traceback for chalmers user errors')
    parser.add_argument('-v', '--verbose',
                        action='store_const', help='print debug information ot the console',
                        dest='log_level',
                        default=logging.INFO, const=logging.DEBUG)
    parser.add_argument('-q', '--quiet',
                        action='store_const', help='Only show warnings or errors the console',
                        dest='log_level', const=logging.WARNING)
    parser.add_argument('--color', action='store_true', default=sys.stdout.isatty(),
                        help='always display with colors')
    parser.add_argument('--no-color', action='store_false', dest='color',
                        help='never display with colors')

    if version:
        parser.add_argument('-V', '--version', action='version',
                            version="%%(prog)s Command line client (version %s)" % (version,))


MODULE_EXTENSIONS = ('.py', '.pyc', '.pyo')

def get_sub_command_names(module):
    return [name for _, name, _ in pkgutil.iter_modules([dirname(module.__file__)]) if not name.startswith('_')]


def get_sub_commands(module):
    names = get_sub_command_names(module)
    this_module = __import__(module.__package__ or module.__name__, fromlist=names)

    for name in names:
        yield getattr(this_module, name)


def add_subparser_modules(parser, module):

    subparsers = parser.add_subparsers(help='commands')

    for command_module in get_sub_commands(module):
        command_module.add_parser(subparsers)

    for key, sub_parser in subparsers.choices.items():
        sub_parser.set_defaults(sub_command_name=key)

def run_command(args, exit=True):

    cli_logger = logging.getLogger('cli-logger')
    cli_logger.error("Command 'chalmers %s'" % getattr(args, 'sub_command_name', '?'))

    try:
        return args.main(args)
    except ShowHelp:
        args.sub_parser.print_help()
        if exit:
            raise SystemExit(1)
        else:
            return 1
