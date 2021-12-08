"""Collection of personal utilities."""

from argparse import ArgumentParser
from typing import Type, TypeVar

from corgy import Corgy, CorgyHelpFormatter

from ._version import __version__
from .logng import conf_logging

_T = TypeVar("_T", bound="Corgy", covariant=True)


def run_prog(
    *sub_corgys: Type[_T],
    formatter_class=CorgyHelpFormatter,
    arg_parser=None,
    add_logging=True,
    add_short_full_helps=True,
    **named_sub_corgys,
):
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
            run_prog(Cmd1, cmd2=Cmd2)


        $ python prog.py --help
        positional arguments:
          cmd        ({'Cmd1'/'cmd2'})

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
        arg_parser: Optional `ArgumentParser` instance to use. If `None` (default), a
            new instance will be created.
        add_logging: Whether to call `logng.conf_logging` to set the log level to
            `INFO`, and add a `--log-level` argument to the parser. Default is `True`.
        add_short_full_helps: Whether to add separate options `--help` and `--helpfull`
            to show help messages, using `CorgyHelpFormatter.add_short_full_helps`.
            Default is `True`.
        **named_sub_corgys: Sub-commands specified as keyword arguments, with the name
            being the name of the sub-command.

    The function will create an `ArgumentParser` instance with sub-parsers corresponding
    to each `Corgy` class in `sub_corgys`. When the program is run, and passed the name
    of a sub-command, a `Corgy` instance will be created with the command line
    arguments, and the instance will be called. The `__call__` method's return value is
    returned.
    """
    if arg_parser is None:
        if not add_short_full_helps:
            arg_parser = ArgumentParser(formatter_class=formatter_class)
        else:
            arg_parser = ArgumentParser(formatter_class=formatter_class, add_help=False)
            CorgyHelpFormatter.add_short_full_helps(arg_parser)
    if add_logging:
        conf_logging(log_level="INFO", arg_parser=arg_parser)

    sub_parsers = arg_parser.add_subparsers(dest="cmd")
    sub_parsers.required = True

    for name, sub_corgy in {
        **{_s.__name__: _s for _s in sub_corgys},
        **named_sub_corgys,
    }.items():
        if not add_short_full_helps:
            sub_parser = sub_parsers.add_parser(name, formatter_class=formatter_class)
        else:
            sub_parser = sub_parsers.add_parser(
                name, formatter_class=formatter_class, add_help=False
            )
            CorgyHelpFormatter.add_short_full_helps(sub_parser)
        sub_parser.set_defaults(corgy=sub_corgy)
        sub_corgy.add_args_to_parser(sub_parser)

    args = arg_parser.parse_args()
    sub_args = args.corgy(**vars(args))
    return sub_args()
