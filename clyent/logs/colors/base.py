import sys
from contextlib import contextmanager
from itertools import chain


class partial_color(object):

    def __init__(self, color_cls, c):
        self.color_cls = color_cls
        self.c = tuple(BaseColor.mkcolor(c))

    def __enter__(self):
        color = self.color_cls
        color.set_colors(color.DEFAULT_STREAM, self.c)

    def __exit__(self, *exc_info):
        color = self.color_cls
        color.set_colors(color.DEFAULT_STREAM, [color.DEFAULT])

    def __call__(self, text):
        color = self.color_cls
        return color(text, self.c)

class color_creator(type):
    def __getattr__(self, attr):
        if hasattr(self, attr.upper()):
            return partial_color(self, getattr(self, attr.upper()))
        else:
            raise AttributeError(attr)

try:
    basestring
except NameError:
    basestring = (str, bytes)

class BaseColor(object):
    __metaclass__ = color_creator

    DEFAULT_STREAM = None

    def __init__(self, text, colors=()):
        self.text = text
        self.colors = tuple(self.mkcolor(colors))

    def __repr__(self):
        return 'color(%r, %r)' % (self.text, self.colors)

    def __enter__(self):
        self.set_colors(self.DEFAULT_STREAM, self.colors)

    def __exit__(self, *exc_info):
        self.set_colors(self.DEFAULT_STREAM, [self.DEFAULT])

    @contextmanager
    def __call__(self, stream, colors=()):

        self.set_colors(stream, chain(self.colors, colors))
        try:
            yield self.text
        finally:
            self.set_colors(stream, [self.DEFAULT])

    @classmethod
    def mkcolor(cls, format_spec):
        if isinstance(format_spec, int):
            yield format_spec
            return

        if isinstance(format_spec, basestring):
            format_spec = format_spec.split(',')
        for c in format_spec:
            if isinstance(c, int):
                yield c
            elif isinstance(c, basestring):
                if c.isdigit():
                    yield int(c)
                elif hasattr(cls, c.upper()):
                    yield getattr(cls, c.upper())

import sys
py3 = sys.version_info.major == 3
if py3:
    # Metaclass hack
    BaseColor = color_creator('BaseColor', (BaseColor,), {})
