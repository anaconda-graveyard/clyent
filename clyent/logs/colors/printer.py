from __future__ import unicode_literals

import string
import sys

from clyent.logs.colors import color


class ColorFormatStream(string.Formatter):

    def __init__(self, stream):
        self.stream = stream or sys.stdout

    def convert_field(self, value, conversion):
        if conversion == 'c':
            return color(value)
        rv = string.Formatter.convert_field(self, value, conversion)
        return rv

    def format_field(self, value, format_spec):
        if isinstance(value , color):
            colors = color.mkcolor(format_spec)
            with value(self.stream, colors) as text:
                self.stream.write(text)
            return
        else:
            rv = string.Formatter.format_field(self, value, format_spec)
            return rv

    def get_field(self, field_name, args, kwargs):
        if field_name.startswith('='):
            return field_name[1:], None
        else:
            return string.Formatter.get_field(self, field_name, args, kwargs)


    def _vformat(self, format_string, args, kwargs, used_args, recursion_depth):
        if recursion_depth < 0:
            raise ValueError('Max string recursion exceeded')
        result = []

        for literal_text, field_name, format_spec, conversion in \
                self.parse(format_string):

            # output the literal text
            self.stream.write(literal_text)

            # if there's a field, output it
            if field_name is not None:
                # this is some markup, find the object and do
                #  the formatting

                # given the field_name, find the object it references
                #  and the argument it came from
                obj, arg_used = self.get_field(field_name, args, kwargs)
                used_args.add(arg_used)

                # do any conversion on the resulting object
                obj = self.convert_field(obj, conversion)

                # expand the format spec, if needed
                format_spec = string.Formatter()._vformat(format_spec, args, kwargs,
                                                          used_args, recursion_depth - 1)

                # format the object and append to the result
                self.format_field(obj, format_spec)

        return ''.join(result)

def print_colors(text='', *args, **kwargs):
    '''
    print_colors(value, ..., sep=' ', end='\n', file=sys.stdout)
    '''

    stream = kwargs.pop('stream', color.DEFAULT_STREAM) or sys.stdout

    end = kwargs.pop('end', '\n')
    sep = kwargs.pop('sep', ' ')
    fmt = ColorFormatStream(stream)

    def write_item(item):
        if isinstance(item, color):
            with item(stream) as text:
                stream.write(text)
        else:
            fmt.vformat(item, (), kwargs)

    if text:
        write_item(text)
    for text in args:
        stream.write(sep)
        write_item(text)

    stream.write(end)

if __name__ == '__main__':

    print_colors('A {=This is an inline \nmessage!c:red,bold,underline} ...')

    print_colors('This is a format substitution {ok!c:green,bold} '
                 'Because the value contains unescaped characters', ok='{OK!}')

    with color.blue:
        print('This is a message within a color context')

    print_colors(color.underline('hello'),
                 'is euqal to',
                 '{=hello!c:underline}')
