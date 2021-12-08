"""Collection of personal utilities."""

from argparse import ArgumentParser
from typing import Type, TypeVar

from corgy import Corgy, CorgyHelpFormatter

from shinyutils._version import __version__

_T = TypeVar("_T", bound="Corgy", covariant=True)


def run_prog(*sub_corgys: Type[_T], formatter_class=CorgyHelpFormatter):
    """Create and run a program with sub-commands defined using `Corgy`.

    Example::

        $ cat prog.py
        from corgy import Corgy
        from shinyutils import run_prog

        class Cmd1(Corgy):
            arg1: int
            arg2: int

            def __call__(self):
                ...

        class Cmd2(Corgy):
            arg1: int

            def __call__(self):
                ...

        if __name__ == "__main__":
            run_prog(Cmd1, Cmd2)


        $ python prog.py --help
        positional arguments:
          cmd        ({'Cmd1'/'Cmd2'})

        options:
          -h/--help  show this help message and exit


        $ python prog.py Cmd1 --help
        options:
        -h/--help   show this help message and exit
        --arg1 int  (required)
        --arg2 int  (required)

    Args:
        *sub_corgys: Sub-commands for the program. Each should be a `Corgy` class, with
            a `__call__` method.
        formatter_class: Class to use for the help formatter. Default is
            `CorgyHelpFormatter`.

    The function will create an `ArgumentParser` instance with sub-parsers corresponding
    to each `Corgy` class in `sub_corgys`. When the program is run, and passed the name
    of a sub-command, a `Corgy` instance will be created with the command line
    arguments, and the instance will be called. The `__call__` method's return value is
    returned.
    """
    arg_parser = ArgumentParser(formatter_class=formatter_class)
    sub_parsers = arg_parser.add_subparsers(dest="cmd")
    sub_parsers.required = True

    for sub_corgy in sub_corgys:
        sub_parser = sub_parsers.add_parser(
            sub_corgy.__name__, formatter_class=formatter_class
        )
        sub_parser.set_defaults(corgy=sub_corgy)
        sub_corgy.add_args_to_parser(sub_parser)

    args = arg_parser.parse_args()
    sub_args = args.corgy(**vars(args))
    return sub_args()
