from __future__ import unicode_literals
from argparse import ArgumentParser
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import os
import sys
from argparse import ArgumentParser
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import os
import sys
import unittest

import mock

import clyent
from clyent import add_subparser_modules
from clyent.colors.color_formatter import print_colors
from clyent.colors import Color, ColorStream

import click
from click.testing import CliRunner

def entry_points(add_parser):
    x = mock.Mock()
    x.load = lambda: add_parser
    return [x]

def add_hello_parser(subparsers):
    subparser = subparsers.add_parser('hello')
    subparser.add_argument('world')
    subparser.set_defaults(main=mock.Mock())

@click.group()
def cli():
    pass

@cli.command()
def initdb():
    click.echo('Initialized the database')

@cli.command()
def dropdb():
    click.echo('Dropped the database')

def add_click_group(subparsers):
    subparser = subparsers.add_parser('cli', click_command=cli)

def add_click_command(subparsers):
    subparser = subparsers.add_parser('initdb', click_command=initdb)

class Test(unittest.TestCase):

    def test_add_subparser_modules(self):
        parser = ArgumentParser()

        with mock.patch('clyent.iter_entry_points') as iter_entry_points:

            ep = mock.Mock()
            ep.load.return_value = add_hello_parser
            iter_entry_points.return_value = [ep]
            add_subparser_modules(parser, None, 'entry_point_name')

        args = parser.parse_args(['hello', 'world'])
        self.assertEqual(args.world, 'world')

    @unittest.skipIf(os.name == 'nt', 'Cannot colorize StringIO on Windows')
    def test_color_format(self):
        output = StringIO()
        output.fileno = lambda: -1
        stream = ColorStream(output)

        print_colors('Are you', '{=okay!c:green}', 'Annie?', file=stream)

        value = output.getvalue()
        output.close()

        self.assertEqual('Are you \033[92mokay\033[0m Annie?\n', value)

    @unittest.skipIf(os.name == 'nt', 'Cannot colorize StringIO on Windows')
    def test_color_context(self):
        output = StringIO()
        output.fileno = lambda: -1
        stream = ColorStream(output)

        with Color('red', stream):
            print_colors('ERROR!', file=stream)

        value = output.getvalue()
        output.close()

        self.assertEqual('\033[91mERROR!\n\033[0m', value)

    @mock.patch('clyent.iter_entry_points')
    def test_click_command(self, iter_entry_points):
        iter_entry_points.return_value = entry_points(add_click_command)

        parser = ArgumentParser(prog='prog')
        add_subparser_modules(parser, None, 'entry_point_name')
        runner = CliRunner()

        with runner.isolation() as out:
            args = parser.parse_args(['initdb'])
            args.main()

        self.assertEqual('Initialized the database\n', out.getvalue())

    @mock.patch('clyent.iter_entry_points')
    def test_click_group(self, iter_entry_points):
        iter_entry_points.return_value = entry_points(add_click_group)

        parser = ArgumentParser(prog='prog')
        add_subparser_modules(parser, None, 'entry_point_name')
        runner = CliRunner()

        with runner.isolation() as out:
            with self.assertRaises(SystemExit):
                args = parser.parse_args(['cli'])

        self.assertEqual('''\
Usage: prog cli [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  dropdb
  initdb
''', out.getvalue())

        with runner.isolation() as out:
            args = parser.parse_args(['cli', 'initdb'])
            args.main()
        self.assertEqual('Initialized the database\n', out.getvalue())

        with runner.isolation() as out:
            args = parser.parse_args(['cli', 'fail'])
            with self.assertRaises(SystemExit):
                args.main()

        self.assertEqual('''\
Usage: prog cli [OPTIONS] COMMAND [ARGS]...

Error: No such command "fail".
''', out.getvalue())


if __name__ == '__main__':
    unittest.main()
