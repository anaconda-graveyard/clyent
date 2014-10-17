Clyent
======

[![Binstar Badge](https://binstar.org/binstar/clyent/badges/build.svg)](https://binstar.org/binstar/clyent/builds)
[![Binstar Badge](https://binstar.org/binstar/clyent/badges/version.svg)](https://binstar.org/binstar/clyent)
[![Binstar Badge](https://binstar.org/binstar/clyent/badges/installer/conda.svg)](https://conda.binstar.org/binstar)

Clyent is a python command line utiliy library for 
[binstar](https://github.com/binstar/binstar_client),
[binstar-build](https://github.com/binstar/binstar-build-client)
and [chalmers](https://github.com/binstar/chalmers)

# Libary Usage:

## `add_default_arguments(parser, version=None)`

Add some default arguments to the argument parser. 

  * `--show-traceback/--hide-traceback

    Show or hide the full traceback for chalmers user errors. Hdden tracebacks are meant for user errors only.
    The error messages will still be printed and the program will exit. 
  
  * `-v/--verbose` or `-q/--quiet`
    
    Switch the amount of output to displat 

  * `--color/--no-color`
    
    Toggle color output

  * `-V/--version
  
    Print version information and exit 
  

## `add_subparser_modules(parser, package)`

This will add sub parsers from a python package e.g. for the directory structure:

```
package/__init__.py
package/commands/__init__.py
package/commands/command.py
```

One would do:
```py

from package import commands
add_subparser_modules(parser, package)

```

Each command module must contain the funciton `add_parser(subparsers)` which takes an argument `subparsers` wich is the result of the function `argparse.ArgumentParser.add_subparsers`

The `add_parser` method should call:
```py
parser = subparsers.add_parser('some-name')
parser.set_defaults(main=your_main_function)
```


## `run_command(parser, exit=True)`

This is 
# Putting this together in a client

```py
```

# print with color on posix and win32

```py

>>> print_colors('Hey! {=This is an inline \nmessage!c:red,bold,underline} ...')
```

<span class="success">Hey! This is an inline 
message</span>

```py
>>> print_colors('This is a format substitution {ok!c:green,bold} '
                 'Because the value contains unescaped characters', ok='{OK!}')

>>> with color.blue:
        print('This is a message within a color context')

>>> print_colors(color.underline('hello'),
                 'is euqal to',
                 '{=hello!c:underline}')
```
